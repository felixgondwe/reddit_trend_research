"""Domain models for Reddit data and analysis."""
from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, HttpUrl


class RedditPost(BaseModel):
    """Model representing a Reddit post."""
    id: str
    title: str
    content: Optional[str] = None
    author: Optional[str] = None  # Anonymized - not stored for privacy
    subreddit: str
    upvotes: int
    comment_count: int
    created_utc: datetime
    url: Optional[HttpUrl] = None  # Not needed for local analysis
    permalink: Optional[str] = None  # Not needed for local analysis
    score: int
    num_comments: int
    
    @property
    def engagement_rate(self) -> float:
        """Calculate engagement rate (upvotes + comments)."""
        return float(self.upvotes + self.num_comments)
    
    @property
    def reddit_link(self) -> Optional[str]:
        """Get full Reddit link (if permalink available)."""
        if self.permalink:
            return f"https://reddit.com{self.permalink}"
        return None


class RedditComment(BaseModel):
    """Model representing a Reddit comment."""
    id: str
    body: str
    author: Optional[str] = None  # Anonymized - not stored for privacy
    upvotes: int
    created_utc: datetime
    post_id: str
    is_top_level: bool = True


class SubredditData(BaseModel):
    """Model representing collected data from a subreddit."""
    subreddit: str
    posts: List[RedditPost]
    comments: List[RedditComment]
    collected_at: datetime
    time_period_days: int
    
    @property
    def total_posts(self) -> int:
        """Get total number of posts."""
        return len(self.posts)
    
    @property
    def total_comments(self) -> int:
        """Get total number of comments."""
        return len(self.comments)


class KeywordFrequency(BaseModel):
    """Model representing keyword frequency analysis."""
    keyword: str
    frequency: int
    subreddits: List[str]
    posts: List[str]  # Post IDs where keyword appears
    trend: str = Field(default="stable", description="rising, stable, or declining")


class TrendingTopic(BaseModel):
    """Model representing a trending topic."""
    topic: str
    mentions: int
    trend: str  # "rising", "stable", "declining", "rapidly_rising"
    subreddits: List[str]
    change_percentage: Optional[float] = None
    posts: List[Dict[str, Any]]  # Post references (anonymized, no author info)


class ExtractedQuestion(BaseModel):
    """Model representing an extracted question."""
    question: str
    frequency: int
    subreddits: List[str]
    posts: List[Dict[str, Any]]  # Post references (anonymized, no author info or links)
    avg_engagement: Dict[str, float]  # avg_upvotes, avg_comments


class AnalysisResult(BaseModel):
    """Model representing analysis results."""
    analysis_date: datetime
    time_period: Dict[str, Any]
    subreddits_analyzed: int
    total_posts: int
    total_comments: int
    trending_topics: List[TrendingTopic]
    common_questions: List[ExtractedQuestion]
    keyword_frequencies: List[KeywordFrequency]
    category_summaries: Dict[str, Any]


class CollectionRequest(BaseModel):
    """Model for requesting data collection."""
    subreddits: Optional[List[str]] = None
    posts_per_subreddit: int = 100
    time_period_days: int = 7
    include_comments: bool = True
    top_comments_limit: int = 10


class CollectionResponse(BaseModel):
    """Model for collection response."""
    success: bool
    message: str
    subreddits_collected: int
    total_posts: int
    total_comments: int
    data_file: str
    collected_at: datetime

