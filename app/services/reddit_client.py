"""Reddit API client with rate limiting and caching."""
import praw
import asyncio
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import logging

from app.config import settings
from app.models.domain import RedditPost, RedditComment
from app.utils.rate_limiter import RateLimiter
from app.utils.cache import CacheManager

logger = logging.getLogger(__name__)


class RedditClient:
    """Reddit API client with compliance guardrails."""
    
    def __init__(self):
        """Initialize Reddit client with PRAW using client credentials."""
        self.reddit = praw.Reddit(
            client_id=settings.reddit_client_id,
            client_secret=settings.reddit_client_secret,
            user_agent=settings.reddit_user_agent
        )
        self.rate_limiter = RateLimiter(settings.rate_limit_requests_per_minute)
        self.cache = CacheManager(
            cache_dir=settings.cache_dir,
            post_expiry_hours=settings.cache_post_expiry_hours,
            comment_expiry_minutes=settings.cache_comment_expiry_minutes
        )
    
    async def _wait_for_rate_limit(self):
        """Wait if needed to maintain rate limit."""
        await self.rate_limiter.wait_if_needed()
    
    def _time_filter_to_reddit(self, days: int) -> str:
        """Convert days to Reddit time filter."""
        if days <= 1:
            return "day"
        elif days <= 7:
            return "week"
        elif days <= 30:
            return "month"
        elif days <= 365:
            return "year"
        else:
            return "all"
    
    async def get_posts(
        self,
        subreddit: str,
        limit: int = 100,
        time_period_days: int = 7
    ) -> List[RedditPost]:
        """
        Get top posts from a subreddit with caching and rate limiting.
        
        Args:
            subreddit: Subreddit name
            limit: Number of posts to fetch
            time_period_days: Number of days to look back
            
        Returns:
            List of RedditPost objects
        """
        time_filter = self._time_filter_to_reddit(time_period_days)
        
        # Check cache first
        cached_posts = self.cache.get_posts(subreddit, limit, time_filter)
        if cached_posts:
            return [RedditPost(**post) for post in cached_posts]
        
        # Wait for rate limit
        await self._wait_for_rate_limit()
        
        try:
            # Fetch from Reddit API
            subreddit_obj = self.reddit.subreddit(subreddit)
            posts = []
            
            # Use hot posts (complies with API - GET /r/{subreddit}/hot)
            for submission in subreddit_obj.hot(limit=limit):
                try:
                    # Filter by time if needed
                    post_time = datetime.fromtimestamp(submission.created_utc)
                    cutoff_time = datetime.now() - timedelta(days=time_period_days)
                    
                    if post_time < cutoff_time and time_filter != "all":
                        continue
                    
                    post = RedditPost(
                        id=submission.id,
                        title=submission.title,
                        content=getattr(submission, 'selftext', None),
                        author=None,  # Anonymized - not stored for privacy
                        subreddit=subreddit,
                        upvotes=submission.score,
                        comment_count=submission.num_comments,
                        created_utc=datetime.fromtimestamp(submission.created_utc),
                        url=None,  # Not needed for local analysis
                        permalink=None,  # Not needed for local analysis
                        score=submission.score,
                        num_comments=submission.num_comments
                    )
                    posts.append(post)
                    
                    if len(posts) >= limit:
                        break
                
                except Exception as e:
                    logger.error(f"Error processing post {submission.id}: {e}")
                    continue
            
            # Cache the results
            posts_data = [post.model_dump() for post in posts]
            self.cache.save_posts(subreddit, posts_data, limit, time_filter)
            
            self.rate_limiter.reset_backoff()
            return posts
        
        except Exception as e:
            # Check if it's a rate limit error (PRAW may raise different exceptions)
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str:
                logger.warning(f"Rate limit exceeded: {e}")
                await self.rate_limiter.handle_rate_limit_error(e)
                # Retry once
                return await self.get_posts(subreddit, limit, time_period_days)
            raise
        
        except Exception as e:
            logger.error(f"Error fetching posts from {subreddit}: {e}")
            raise
    
    async def get_comments(
        self,
        post_id: str,
        subreddit: str,
        limit: int = 10
    ) -> List[RedditComment]:
        """
        Get top comments from a post with caching and rate limiting.
        
        Args:
            post_id: Reddit post ID
            subreddit: Subreddit name
            limit: Number of top comments to fetch
            
        Returns:
            List of RedditComment objects
        """
        # Check cache first
        cached_comments = self.cache.get_comments(post_id, limit)
        if cached_comments:
            return [RedditComment(**comment) for comment in cached_comments]
        
        # Wait for rate limit
        await self._wait_for_rate_limit()
        
        try:
            # Fetch from Reddit API (GET /r/{subreddit}/comments/{article})
            submission = self.reddit.submission(id=post_id)
            submission.comments.replace_more(limit=0)  # Remove "more comments" placeholders
            
            comments = []
            for comment in submission.comments.list()[:limit]:
                try:
                    # Only get top-level comments
                    if hasattr(comment, 'parent_id') and comment.parent_id.startswith('t3_'):
                        reddit_comment = RedditComment(
                            id=comment.id,
                            body=comment.body,
                            author=None,  # Anonymized - not stored for privacy
                            upvotes=comment.score,
                            created_utc=datetime.fromtimestamp(comment.created_utc),
                            post_id=post_id,
                            is_top_level=True
                        )
                        comments.append(reddit_comment)
                        
                        if len(comments) >= limit:
                            break
                except Exception as e:
                    logger.error(f"Error processing comment {comment.id}: {e}")
                    continue
            
            # Cache the results
            comments_data = [comment.model_dump() for comment in comments]
            self.cache.save_comments(post_id, comments_data, limit)
            
            self.rate_limiter.reset_backoff()
            return comments
        
        except Exception as e:
            # Check if it's a rate limit error (PRAW may raise different exceptions)
            error_str = str(e).lower()
            if "rate limit" in error_str or "429" in error_str:
                logger.warning(f"Rate limit exceeded: {e}")
                await self.rate_limiter.handle_rate_limit_error(e)
                # Retry once
                return await self.get_comments(post_id, subreddit, limit)
            raise
        
        except Exception as e:
            logger.error(f"Error fetching comments for post {post_id}: {e}")
            return []  # Return empty list on error, don't fail completely
    
    async def collect_subreddit_data(
        self,
        subreddit: str,
        posts_per_subreddit: int = 100,
        time_period_days: int = 7,
        include_comments: bool = True,
        top_comments_limit: int = 10
    ) -> Dict[str, Any]:
        """
        Collect all data from a subreddit.
        
        Args:
            subreddit: Subreddit name
            posts_per_subreddit: Number of posts to fetch
            time_period_days: Days to look back
            include_comments: Whether to fetch comments
            top_comments_limit: Number of top comments per post
            
        Returns:
            Dictionary with posts and comments
        """
        logger.info(f"Collecting data from r/{subreddit}")
        
        # Get posts
        posts = await self.get_posts(subreddit, posts_per_subreddit, time_period_days)
        
        # Get comments if requested
        comments = []
        if include_comments:
            for post in posts:
                post_comments = await self.get_comments(post.id, subreddit, top_comments_limit)
                comments.extend(post_comments)
                # Small delay between comment fetches
                await asyncio.sleep(0.1)
        
        return {
            "subreddit": subreddit,
            "posts": [post.model_dump() for post in posts],
            "comments": [comment.model_dump() for comment in comments],
            "collected_at": datetime.now().isoformat(),
            "time_period_days": time_period_days
        }

