"""FastAPI main application."""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from app.config import settings
from app.models.domain import CollectionRequest, CollectionResponse, AnalysisResult
from app.services.reddit_client import RedditClient
from app.services.analysis_service import AnalysisService
from app.services.data_storage import DataStorage

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Reddit Trend Research API",
    description="API for collecting and analyzing Reddit data to stay up to date with communities I care about (AI trends and fitness)",
    version="1.0.0"
)

# CORS middleware for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
reddit_client = RedditClient()
analysis_service = AnalysisService()
data_storage = DataStorage()


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Reddit Trend Research API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "rate_limit_remaining": reddit_client.rate_limiter.get_remaining_requests()
    }


@app.post("/collect", response_model=CollectionResponse)
async def collect_data(
    request: CollectionRequest,
    background_tasks: BackgroundTasks
):
    """
    Collect data from Reddit subreddits.
    
    This endpoint collects posts and comments from specified subreddits
    with rate limiting and caching compliance.
    """
    try:
        # Use default subreddits if none specified
        subreddits = request.subreddits or settings.all_subreddits
        
        logger.info(f"Starting collection for {len(subreddits)} subreddits")
        
        all_posts = []
        all_comments = []
        collected_subreddits = []
        
        # Collect data from each subreddit
        for subreddit in subreddits:
            try:
                data = await reddit_client.collect_subreddit_data(
                    subreddit=subreddit,
                    posts_per_subreddit=request.posts_per_subreddit,
                    time_period_days=request.time_period_days,
                    include_comments=request.include_comments,
                    top_comments_limit=request.top_comments_limit
                )
                
                all_posts.extend(data["posts"])
                all_comments.extend(data["comments"])
                collected_subreddits.append(subreddit)
                
                logger.info(f"Collected {len(data['posts'])} posts from r/{subreddit}")
            
            except Exception as e:
                logger.error(f"Error collecting from r/{subreddit}: {e}")
                continue
        
        # Combine all data
        combined_data = {
            "subreddits": collected_subreddits,
            "posts": all_posts,
            "comments": all_comments,
            "collected_at": datetime.now().isoformat(),
            "time_period_days": request.time_period_days
        }
        
        # Save to file
        filename = data_storage.save_collected_data(combined_data)
        
        # Auto-analyze the collected data
        try:
            analysis_result = analysis_service.analyze_data(combined_data)
            analysis_file = data_storage.save_analysis_result(analysis_result)
            logger.info(f"Auto-analyzed data: {analysis_file}")
        except Exception as e:
            logger.warning(f"Auto-analysis failed: {e}")
        
        # Clean expired cache in background
        background_tasks.add_task(reddit_client.cache.clear_expired)
        
        return CollectionResponse(
            success=True,
            message=f"Successfully collected data from {len(collected_subreddits)} subreddits",
            subreddits_collected=len(collected_subreddits),
            total_posts=len(all_posts),
            total_comments=len(all_comments),
            data_file=filename,
            collected_at=datetime.now()
        )
    
    except Exception as e:
        logger.error(f"Error in collection: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze")
async def analyze_data(data_file: str):
    """
    Analyze collected data.
    
    Args:
        data_file: Name of the data file to analyze
    """
    try:
        # Load collected data
        collected_data = data_storage.load_collected_data(data_file)
        
        if not collected_data:
            raise HTTPException(status_code=404, detail=f"Data file not found: {data_file}")
        
        # Perform analysis
        analysis_result = analysis_service.analyze_data(collected_data)
        
        # Save analysis result
        analysis_file = data_storage.save_analysis_result(analysis_result)
        
        return {
            "success": True,
            "analysis_file": analysis_file,
            "result": analysis_result.model_dump()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/data/files")
async def list_data_files():
    """List all collected data files."""
    return {
        "data_files": data_storage.list_collected_data(),
        "analysis_files": data_storage.list_analysis_results()
    }


@app.get("/data/{filename}")
async def get_data_file(filename: str):
    """Get a specific data file."""
    data = data_storage.load_collected_data(filename)
    if not data:
        analysis = data_storage.load_analysis_result(filename)
        if not analysis:
            raise HTTPException(status_code=404, detail="File not found")
        return analysis
    return data


@app.get("/analysis/latest")
async def get_latest_analysis():
    """Get the most recent analysis result."""
    analysis = data_storage.get_latest_analysis()
    if not analysis:
        raise HTTPException(status_code=404, detail="No analysis results found")
    return analysis


@app.get("/subreddits")
async def get_subreddits():
    """Get list of target subreddits."""
    return {
        "ai_ml": settings.ai_ml_subreddits,
        "running": settings.running_subreddits,
        "nutrition": settings.nutrition_subreddits,
        "strength_training": settings.strength_training_subreddits,
        "all": settings.all_subreddits
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)

