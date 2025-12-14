"""Pytest configuration and fixtures."""
import pytest
import os
from unittest.mock import Mock, AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
from pathlib import Path
import tempfile
import shutil

# Set test environment variables before importing app modules
os.environ["REDDIT_CLIENT_ID"] = "test_client_id"
os.environ["REDDIT_CLIENT_SECRET"] = "test_client_secret"
os.environ["REDDIT_USER_AGENT"] = "test:reddit_trend_research:v1.0.0 (by /u/test_user)"
os.environ["DATA_DIR"] = "test_data"
os.environ["REPORTS_DIR"] = "test_data/reports"
os.environ["CACHE_DIR"] = "test_data/cache"

from fastapi.testclient import TestClient
from app.api.main import app
from app.models.domain import RedditPost, RedditComment


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def temp_data_dir():
    """Create temporary data directory."""
    temp_dir = tempfile.mkdtemp()
    os.makedirs(f"{temp_dir}/reports", exist_ok=True)
    os.makedirs(f"{temp_dir}/cache", exist_ok=True)
    
    # Patch settings
    with patch("app.config.settings.data_dir", temp_dir):
        with patch("app.config.settings.reports_dir", f"{temp_dir}/reports"):
            with patch("app.config.settings.cache_dir", f"{temp_dir}/cache"):
                yield temp_dir
    
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_reddit_submission():
    """Create a mock Reddit submission."""
    submission = Mock()
    submission.id = "test_post_123"
    submission.title = "Test Post Title"
    submission.selftext = "Test post content"
    submission.author = Mock()
    submission.author.__str__ = Mock(return_value="test_user")
    submission.score = 100
    submission.num_comments = 50
    submission.created_utc = (datetime.now() - timedelta(days=1)).timestamp()
    submission.url = "https://example.com"
    submission.permalink = "/r/test/comments/test_post_123"
    return submission


@pytest.fixture
def mock_reddit_comment():
    """Create a mock Reddit comment."""
    comment = Mock()
    comment.id = "test_comment_123"
    comment.body = "This is a test comment"
    comment.author = Mock()
    comment.author.__str__ = Mock(return_value="test_commenter")
    comment.score = 10
    comment.created_utc = (datetime.now() - timedelta(hours=12)).timestamp()
    comment.parent_id = "t3_test_post_123"  # Top-level comment
    return comment


@pytest.fixture
def mock_reddit_subreddit(mock_reddit_submission):
    """Create a mock Reddit subreddit."""
    subreddit = Mock()
    subreddit.hot = Mock(return_value=[mock_reddit_submission])
    return subreddit


@pytest.fixture
def mock_reddit_client(mock_reddit_submission, mock_reddit_comment, mock_reddit_subreddit):
    """Create a mock Reddit client."""
    mock_reddit = Mock()
    mock_reddit.subreddit = Mock(return_value=mock_reddit_subreddit)
    
    # Mock submission for comments
    mock_submission = Mock()
    mock_submission.id = "test_post_123"
    mock_submission.comments = Mock()
    mock_submission.comments.list = Mock(return_value=[mock_reddit_comment])
    mock_submission.comments.replace_more = Mock()
    mock_reddit.submission = Mock(return_value=mock_submission)
    
    return mock_reddit


@pytest.fixture
def sample_reddit_post():
    """Create a sample RedditPost."""
    return RedditPost(
        id="test_post_123",
        title="Test Post Title",
        content="Test post content",
        author="test_user",
        subreddit="test",
        upvotes=100,
        comment_count=50,
        created_utc=datetime.now() - timedelta(days=1),
        url="https://example.com",
        permalink="/r/test/comments/test_post_123",
        score=100,
        num_comments=50
    )


@pytest.fixture
def sample_reddit_comment():
    """Create a sample RedditComment."""
    return RedditComment(
        id="test_comment_123",
        body="This is a test comment",
        author="test_commenter",
        upvotes=10,
        created_utc=datetime.now() - timedelta(hours=12),
        post_id="test_post_123",
        is_top_level=True
    )


@pytest.fixture
def sample_collected_data(sample_reddit_post, sample_reddit_comment):
    """Create sample collected data."""
    return {
        "subreddits": ["test"],
        "posts": [sample_reddit_post.model_dump()],
        "comments": [sample_reddit_comment.model_dump()],
        "collected_at": datetime.now().isoformat(),
        "time_period_days": 7
    }


@pytest.fixture
def mock_rate_limiter():
    """Create a mock rate limiter."""
    limiter = AsyncMock()
    limiter.wait_if_needed = AsyncMock()
    limiter.handle_rate_limit_error = AsyncMock(return_value=1)
    limiter.reset_backoff = Mock()
    limiter.get_remaining_requests = Mock(return_value=60)
    return limiter


@pytest.fixture
def mock_cache_manager():
    """Create a mock cache manager."""
    cache = Mock()
    cache.get_posts = Mock(return_value=None)
    cache.save_posts = Mock()
    cache.get_comments = Mock(return_value=None)
    cache.save_comments = Mock()
    cache.clear_expired = Mock()
    return cache

