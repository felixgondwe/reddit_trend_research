"""Unit tests for RedditClient."""
import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta

from app.services.reddit_client import RedditClient
from app.models.domain import RedditPost, RedditComment


class TestRedditClient:
    """Tests for RedditClient."""
    
    @pytest.fixture
    def mock_praw_reddit(self):
        """Mock PRAW Reddit instance."""
        with patch("app.services.reddit_client.praw.Reddit") as mock_reddit_class:
            mock_reddit = Mock()
            mock_reddit_class.return_value = mock_reddit
            yield mock_reddit
    
    @pytest.fixture
    def reddit_client(self, mock_praw_reddit):
        """Create RedditClient instance."""
        with patch("app.services.reddit_client.settings") as mock_settings:
            mock_settings.reddit_client_id = "test_id"
            mock_settings.reddit_client_secret = "test_secret"
            mock_settings.reddit_user_agent = "test:agent:v1.0"
            mock_settings.rate_limit_requests_per_minute = 60
            mock_settings.cache_dir = "test_cache"
            mock_settings.cache_post_expiry_hours = 1
            mock_settings.cache_comment_expiry_minutes = 30
            
            client = RedditClient()
            client.reddit = mock_praw_reddit
            return client
    
    @pytest.fixture
    def mock_submission(self):
        """Create mock Reddit submission."""
        submission = Mock()
        submission.id = "test123"
        submission.title = "Test Post"
        submission.selftext = "Test content"
        submission.author = Mock()
        submission.author.__str__ = Mock(return_value="test_user")
        submission.score = 100
        submission.num_comments = 50
        submission.created_utc = (datetime.now() - timedelta(days=1)).timestamp()
        submission.url = "https://example.com"
        submission.permalink = "/r/test/comments/test123"
        return submission
    
    @pytest.fixture
    def mock_comment(self):
        """Create mock Reddit comment."""
        comment = Mock()
        comment.id = "comment123"
        comment.body = "Test comment"
        comment.author = Mock()
        comment.author.__str__ = Mock(return_value="test_commenter")
        comment.score = 10
        comment.created_utc = (datetime.now() - timedelta(hours=12)).timestamp()
        comment.parent_id = "t3_test123"
        return comment
    
    @pytest.mark.asyncio
    async def test_get_posts(self, reddit_client, mock_submission):
        """Test getting posts from subreddit."""
        # Mock subreddit
        mock_subreddit = Mock()
        mock_subreddit.hot = Mock(return_value=[mock_submission])
        reddit_client.reddit.subreddit = Mock(return_value=mock_subreddit)
        
        # Mock cache to return None (cache miss)
        reddit_client.cache.get_posts = Mock(return_value=None)
        reddit_client.cache.save_posts = Mock()
        
        # Mock rate limiter
        reddit_client.rate_limiter.wait_if_needed = AsyncMock()
        reddit_client.rate_limiter.reset_backoff = Mock()
        
        posts = await reddit_client.get_posts("test", limit=10, time_period_days=7)
        
        assert len(posts) == 1
        assert posts[0].id == "test123"
        assert posts[0].title == "Test Post"
        reddit_client.cache.save_posts.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_posts_from_cache(self, reddit_client):
        """Test getting posts from cache."""
        from datetime import datetime
        cached_data = [{
            "id": "cached123",
            "title": "Cached Post",
            "content": None,
            "author": "cached_user",
            "subreddit": "test",
            "upvotes": 50,
            "comment_count": 25,
            "created_utc": datetime.now().isoformat(),
            "url": "https://example.com",
            "permalink": "/r/test/comments/cached123",
            "score": 50,
            "num_comments": 25
        }]
        
        reddit_client.cache.get_posts = Mock(return_value=cached_data)
        
        posts = await reddit_client.get_posts("test", limit=10, time_period_days=7)
        
        assert len(posts) == 1
        assert posts[0].id == "cached123"
        # Should not call Reddit API
        if hasattr(reddit_client.reddit, 'subreddit'):
            reddit_client.reddit.subreddit.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_get_posts_rate_limit(self, reddit_client, mock_submission):
        """Test handling rate limit errors."""
        # Create a custom rate limit exception
        class RateLimitExceeded(Exception):
            pass
        
        # Mock subreddit to raise rate limit error
        mock_subreddit = Mock()
        mock_subreddit.hot = Mock(side_effect=RateLimitExceeded("Rate limited"))
        reddit_client.reddit.subreddit = Mock(return_value=mock_subreddit)
        
        # Mock cache
        reddit_client.cache.get_posts = Mock(return_value=None)
        
        # Mock rate limiter
        reddit_client.rate_limiter.wait_if_needed = AsyncMock()
        reddit_client.rate_limiter.handle_rate_limit_error = AsyncMock(return_value=1)
        
        # The method should catch the rate limit error and retry
        # On retry it will fail again, so we expect an exception
        with pytest.raises((RateLimitExceeded, Exception)):
            await reddit_client.get_posts("test", limit=10, time_period_days=7)
        
        # Verify rate limit error handler was called
        assert reddit_client.rate_limiter.handle_rate_limit_error.called
    
    @pytest.mark.asyncio
    async def test_get_comments(self, reddit_client, mock_comment):
        """Test getting comments from a post."""
        # Mock submission
        mock_submission = Mock()
        mock_submission.id = "test123"
        mock_submission.comments = Mock()
        mock_submission.comments.list = Mock(return_value=[mock_comment])
        mock_submission.comments.replace_more = Mock()
        reddit_client.reddit.submission = Mock(return_value=mock_submission)
        
        # Mock cache
        reddit_client.cache.get_comments = Mock(return_value=None)
        reddit_client.cache.save_comments = Mock()
        
        # Mock rate limiter
        reddit_client.rate_limiter.wait_if_needed = AsyncMock()
        reddit_client.rate_limiter.reset_backoff = Mock()
        
        comments = await reddit_client.get_comments("test123", "test", limit=10)
        
        assert len(comments) == 1
        assert comments[0].id == "comment123"
        assert comments[0].body == "Test comment"
        reddit_client.cache.save_comments.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_get_comments_from_cache(self, reddit_client):
        """Test getting comments from cache."""
        from datetime import datetime
        cached_data = [{
            "id": "cached_comment",
            "body": "Cached comment",
            "author": "cached_user",
            "upvotes": 5,
            "created_utc": datetime.now().isoformat(),
            "post_id": "test123",
            "is_top_level": True
        }]
        
        reddit_client.cache.get_comments = Mock(return_value=cached_data)
        
        comments = await reddit_client.get_comments("test123", "test", limit=10)
        
        assert len(comments) == 1
        assert comments[0].id == "cached_comment"
        # Should not call Reddit API
        if hasattr(reddit_client.reddit, 'submission'):
            reddit_client.reddit.submission.assert_not_called()
    
    @pytest.mark.asyncio
    async def test_collect_subreddit_data(self, reddit_client, mock_submission, mock_comment):
        """Test collecting complete subreddit data."""
        # Mock subreddit
        mock_subreddit = Mock()
        mock_subreddit.hot = Mock(return_value=[mock_submission])
        reddit_client.reddit.subreddit = Mock(return_value=mock_subreddit)
        
        # Mock submission for comments
        mock_submission_obj = Mock()
        mock_submission_obj.id = "test123"
        mock_submission_obj.comments = Mock()
        mock_submission_obj.comments.list = Mock(return_value=[mock_comment])
        mock_submission_obj.comments.replace_more = Mock()
        reddit_client.reddit.submission = Mock(return_value=mock_submission_obj)
        
        # Mock cache
        reddit_client.cache.get_posts = Mock(return_value=None)
        reddit_client.cache.get_comments = Mock(return_value=None)
        reddit_client.cache.save_posts = Mock()
        reddit_client.cache.save_comments = Mock()
        
        # Mock rate limiter
        reddit_client.rate_limiter.wait_if_needed = AsyncMock()
        reddit_client.rate_limiter.reset_backoff = Mock()
        
        data = await reddit_client.collect_subreddit_data(
            "test",
            posts_per_subreddit=10,
            time_period_days=7,
            include_comments=True,
            top_comments_limit=10
        )
        
        assert data["subreddit"] == "test"
        assert len(data["posts"]) == 1
        assert len(data["comments"]) == 1
        assert "collected_at" in data
    
    def test_time_filter_conversion(self, reddit_client):
        """Test time filter conversion."""
        assert reddit_client._time_filter_to_reddit(1) == "day"
        assert reddit_client._time_filter_to_reddit(7) == "week"
        assert reddit_client._time_filter_to_reddit(30) == "month"
        assert reddit_client._time_filter_to_reddit(365) == "year"
        assert reddit_client._time_filter_to_reddit(1000) == "all"

