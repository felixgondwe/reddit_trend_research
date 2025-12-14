"""Rate limiting utilities for Reddit API compliance."""
import time
import asyncio
from datetime import datetime, timedelta
from typing import Optional
from collections import deque
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """Rate limiter implementing Reddit's 60 requests/minute limit with exponential backoff."""
    
    def __init__(self, requests_per_minute: int = 60):
        """
        Initialize rate limiter.
        
        Args:
            requests_per_minute: Maximum requests per minute (default: 60 for Reddit)
        """
        self.requests_per_minute = requests_per_minute
        self.request_times: deque = deque()
        self.min_interval = 60.0 / requests_per_minute  # Minimum seconds between requests
        self.backoff_delay = 1  # Start with 1 second backoff
        
    def _clean_old_requests(self):
        """Remove request timestamps older than 1 minute."""
        one_minute_ago = time.time() - 60
        while self.request_times and self.request_times[0] < one_minute_ago:
            self.request_times.popleft()
    
    async def wait_if_needed(self):
        """
        Wait if necessary to maintain rate limit.
        
        This should be called before each API request.
        """
        self._clean_old_requests()
        
        # If we're at the limit, wait until we can make another request
        if len(self.request_times) >= self.requests_per_minute:
            oldest_request = self.request_times[0]
            wait_time = 60 - (time.time() - oldest_request) + 0.1  # Small buffer
            if wait_time > 0:
                logger.info(f"Rate limit reached. Waiting {wait_time:.2f} seconds...")
                await asyncio.sleep(wait_time)
                self._clean_old_requests()
        
        # Ensure minimum interval between requests
        if self.request_times:
            last_request = self.request_times[-1]
            elapsed = time.time() - last_request
            if elapsed < self.min_interval:
                wait_time = self.min_interval - elapsed
                await asyncio.sleep(wait_time)
        
        # Record this request
        self.request_times.append(time.time())
    
    async def handle_rate_limit_error(self, error: Exception):
        """
        Handle rate limit error with exponential backoff.
        
        Args:
            error: The rate limit error from Reddit API
            
        Returns:
            The delay to wait before retrying
        """
        delay = min(self.backoff_delay, 60)  # Cap at 60 seconds
        logger.warning(f"Rate limit error encountered. Waiting {delay} seconds with exponential backoff...")
        await asyncio.sleep(delay)
        
        # Exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s, 60s max
        self.backoff_delay = min(self.backoff_delay * 2, 60)
        
        return delay
    
    def reset_backoff(self):
        """Reset backoff delay after successful request."""
        self.backoff_delay = 1
    
    def get_remaining_requests(self) -> int:
        """Get number of requests remaining in current minute."""
        self._clean_old_requests()
        return max(0, self.requests_per_minute - len(self.request_times))

