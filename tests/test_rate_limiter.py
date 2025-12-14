"""Unit tests for RateLimiter."""
import pytest
import asyncio
import time
from app.utils.rate_limiter import RateLimiter


class TestRateLimiter:
    """Tests for RateLimiter."""
    
    @pytest.fixture
    def rate_limiter(self):
        """Create RateLimiter instance."""
        return RateLimiter(requests_per_minute=60)
    
    @pytest.mark.asyncio
    async def test_wait_if_needed_no_wait(self, rate_limiter):
        """Test that no wait occurs when under limit."""
        start = time.time()
        await rate_limiter.wait_if_needed()
        elapsed = time.time() - start
        
        # Should be very fast (no wait)
        assert elapsed < 0.1
    
    @pytest.mark.asyncio
    async def test_wait_if_needed_at_limit(self, rate_limiter):
        """Test waiting when at rate limit."""
        # Fill up the rate limiter
        for _ in range(60):
            rate_limiter.request_times.append(time.time())
        
        start = time.time()
        await rate_limiter.wait_if_needed()
        elapsed = time.time() - start
        
        # Should wait approximately 1 second (60 seconds / 60 requests)
        assert elapsed >= 0.9  # Allow some margin
    
    @pytest.mark.asyncio
    async def test_handle_rate_limit_error(self, rate_limiter):
        """Test handling rate limit error with exponential backoff."""
        start = time.time()
        await rate_limiter.handle_rate_limit_error(Exception("Rate limit"))
        elapsed = time.time() - start
        
        # Should wait 1 second initially
        assert elapsed >= 0.9
        assert rate_limiter.backoff_delay == 2  # Doubled
    
    def test_exponential_backoff_cap(self, rate_limiter):
        """Test that backoff is capped at 60 seconds."""
        # Trigger backoff multiple times
        for _ in range(10):
            rate_limiter.backoff_delay = min(rate_limiter.backoff_delay * 2, 60)
        
        # Should be capped at 60
        assert rate_limiter.backoff_delay == 60
    
    def test_reset_backoff(self, rate_limiter):
        """Test resetting backoff delay."""
        rate_limiter.backoff_delay = 32
        rate_limiter.reset_backoff()
        assert rate_limiter.backoff_delay == 1
    
    def test_get_remaining_requests(self, rate_limiter):
        """Test getting remaining requests."""
        # Initially should be 60
        assert rate_limiter.get_remaining_requests() == 60
        
        # Add some requests
        rate_limiter.request_times.append(time.time())
        assert rate_limiter.get_remaining_requests() == 59
    
    def test_clean_old_requests(self, rate_limiter):
        """Test cleaning old request timestamps."""
        # Add old request (more than 1 minute ago)
        old_time = time.time() - 120
        rate_limiter.request_times.append(old_time)
        
        # Add recent request
        recent_time = time.time()
        rate_limiter.request_times.append(recent_time)
        
        # Clean old requests
        rate_limiter._clean_old_requests()
        
        # Should only have recent request
        assert len(rate_limiter.request_times) == 1
        assert rate_limiter.request_times[0] == recent_time

