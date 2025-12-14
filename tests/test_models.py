"""Tests for domain models."""
import pytest
from datetime import datetime
from app.models.domain import RedditPost, RedditComment, KeywordFrequency


def test_reddit_post_engagement_rate():
    """Test engagement rate calculation."""
    post = RedditPost(
        id="test123",
        title="Test Post",
        content="Test content",
        author="test_user",
        subreddit="test",
        upvotes=100,
        comment_count=50,
        created_utc=datetime.now(),
        url="https://example.com",
        permalink="/r/test/comments/test123",
        score=100,
        num_comments=50
    )
    
    assert post.engagement_rate == 150.0


def test_keyword_frequency():
    """Test keyword frequency model."""
    keyword = KeywordFrequency(
        keyword="test",
        frequency=10,
        subreddits=["test1", "test2"],
        posts=["post1", "post2"]
    )
    
    assert keyword.keyword == "test"
    assert keyword.frequency == 10
    assert len(keyword.subreddits) == 2

