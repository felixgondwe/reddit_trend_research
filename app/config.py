"""Application configuration settings."""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Reddit API Credentials
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str = "python:reddit_trend_research:v1.0.0 (by /u/reddit_user)"
    
    # API Settings
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    streamlit_port: int = 8501
    
    # Rate Limiting
    rate_limit_requests_per_minute: int = 60
    cache_post_expiry_hours: int = 1
    cache_comment_expiry_minutes: int = 30
    
    # Data Storage
    data_dir: str = "app/data"
    reports_dir: str = "app/data/reports"
    cache_dir: str = "app/data/cache"
    
    # Analysis Settings
    default_posts_per_subreddit: int = 100
    default_time_period_days: int = 7
    top_comments_limit: int = 10
    
    # Target Subreddits
    ai_ml_subreddits: List[str] = [
        "ChatGPT",
        "MachineLearning",
        "artificial",
        "learnmachinelearning",
        "OpenAI",
        "ArtificialIntelligence",
        "datascience",
        "deeplearning",
        "LocalLLaMA",
        "AIPromptProgramming"
    ]
    
    running_subreddits: List[str] = [
        "running",
        "AdvancedRunning",
        "RunningShoeGeeks",
        "C25K",
        "ultrarunning"
    ]
    
    nutrition_subreddits: List[str] = [
        "nutrition",
        "EatCheapAndHealthy",
        "keto",
        "loseit",
        "fitmeals"
    ]
    
    strength_training_subreddits: List[str] = [
        "weightroom",
        "bodybuilding",
        "Fitness",
        "gainit",
        "naturalbodybuilding"
    ]
    
    @property
    def all_subreddits(self) -> List[str]:
        """Get all target subreddits."""
        return (
            self.ai_ml_subreddits +
            self.running_subreddits +
            self.nutrition_subreddits +
            self.strength_training_subreddits
        )
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

