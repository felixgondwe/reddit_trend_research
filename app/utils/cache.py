"""Caching utilities for Reddit API data."""
import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List
import hashlib
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """Manages local caching of Reddit API data."""
    
    def __init__(self, cache_dir: str, post_expiry_hours: int = 1, comment_expiry_minutes: int = 30):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
            post_expiry_hours: Hours until post cache expires (default: 1)
            comment_expiry_minutes: Minutes until comment cache expires (default: 30)
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.post_expiry = timedelta(hours=post_expiry_hours)
        self.comment_expiry = timedelta(minutes=comment_expiry_minutes)
    
    def _get_cache_key(self, subreddit: str, cache_type: str, **kwargs) -> str:
        """Generate cache key for a request."""
        key_parts = [subreddit, cache_type]
        for k, v in sorted(kwargs.items()):
            key_parts.append(f"{k}:{v}")
        key_string = "_".join(key_parts)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _get_cache_path(self, cache_key: str) -> Path:
        """Get file path for cache key."""
        return self.cache_dir / f"{cache_key}.json"
    
    def _is_expired(self, cache_data: Dict[str, Any], expiry: timedelta) -> bool:
        """Check if cache entry is expired."""
        cached_at = datetime.fromisoformat(cache_data.get("cached_at", ""))
        return datetime.now() - cached_at > expiry
    
    def get_posts(self, subreddit: str, limit: int = 100, time_filter: str = "week") -> Optional[List[Dict[str, Any]]]:
        """
        Get cached posts if available and not expired.
        
        Args:
            subreddit: Subreddit name
            limit: Number of posts requested
            time_filter: Time filter (day, week, month, year, all)
            
        Returns:
            Cached posts or None if not cached/expired
        """
        cache_key = self._get_cache_key(subreddit, "posts", limit=limit, time_filter=time_filter)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            if self._is_expired(cache_data, self.post_expiry):
                logger.info(f"Cache expired for {subreddit} posts")
                cache_path.unlink()  # Delete expired cache
                return None
            
            logger.info(f"Cache hit for {subreddit} posts")
            return cache_data.get("data", [])
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None
    
    def save_posts(self, subreddit: str, posts: List[Dict[str, Any]], limit: int = 100, time_filter: str = "week"):
        """
        Save posts to cache.
        
        Args:
            subreddit: Subreddit name
            posts: List of post data
            limit: Number of posts
            time_filter: Time filter used
        """
        cache_key = self._get_cache_key(subreddit, "posts", limit=limit, time_filter=time_filter)
        cache_path = self._get_cache_path(cache_key)
        
        cache_data = {
            "cached_at": datetime.now().isoformat(),
            "subreddit": subreddit,
            "data": posts
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
            logger.info(f"Cached {len(posts)} posts for {subreddit}")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def get_comments(self, post_id: str, limit: int = 10) -> Optional[List[Dict[str, Any]]]:
        """
        Get cached comments if available and not expired.
        
        Args:
            post_id: Reddit post ID
            limit: Number of comments requested
            
        Returns:
            Cached comments or None if not cached/expired
        """
        cache_key = self._get_cache_key(post_id, "comments", limit=limit)
        cache_path = self._get_cache_path(cache_key)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r') as f:
                cache_data = json.load(f)
            
            if self._is_expired(cache_data, self.comment_expiry):
                logger.info(f"Cache expired for post {post_id} comments")
                cache_path.unlink()  # Delete expired cache
                return None
            
            logger.info(f"Cache hit for post {post_id} comments")
            return cache_data.get("data", [])
        except Exception as e:
            logger.error(f"Error reading cache: {e}")
            return None
    
    def save_comments(self, post_id: str, comments: List[Dict[str, Any]], limit: int = 10):
        """
        Save comments to cache.
        
        Args:
            post_id: Reddit post ID
            comments: List of comment data
            limit: Number of comments
        """
        cache_key = self._get_cache_key(post_id, "comments", limit=limit)
        cache_path = self._get_cache_path(cache_key)
        
        cache_data = {
            "cached_at": datetime.now().isoformat(),
            "post_id": post_id,
            "data": comments
        }
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(cache_data, f, indent=2, default=str)
            logger.info(f"Cached {len(comments)} comments for post {post_id}")
        except Exception as e:
            logger.error(f"Error saving cache: {e}")
    
    def clear_cache(self):
        """Clear all cache files."""
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                cache_file.unlink()
            logger.info("Cache cleared")
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
    
    def clear_expired(self):
        """Clear only expired cache files."""
        cleared = 0
        try:
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, 'r') as f:
                        cache_data = json.load(f)
                    
                    cached_at = datetime.fromisoformat(cache_data.get("cached_at", ""))
                    
                    # Determine expiry based on cache type
                    if "posts" in cache_data:
                        expiry = self.post_expiry
                    else:
                        expiry = self.comment_expiry
                    
                    if datetime.now() - cached_at > expiry:
                        cache_file.unlink()
                        cleared += 1
                except Exception:
                    # If we can't read it, delete it
                    cache_file.unlink()
                    cleared += 1
            
            if cleared > 0:
                logger.info(f"Cleared {cleared} expired cache files")
        except Exception as e:
            logger.error(f"Error clearing expired cache: {e}")

