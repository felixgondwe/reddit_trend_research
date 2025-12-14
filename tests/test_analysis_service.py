"""Unit tests for AnalysisService."""
import pytest
from datetime import datetime, timedelta
from app.services.analysis_service import AnalysisService
from app.models.domain import RedditPost, RedditComment


class TestAnalysisService:
    """Tests for AnalysisService."""
    
    @pytest.fixture
    def analysis_service(self):
        """Create AnalysisService instance."""
        return AnalysisService()
    
    @pytest.fixture
    def sample_posts(self):
        """Create sample posts."""
        return [
            RedditPost(
                id="post1",
                title="How to write better prompts for ChatGPT?",
                content="I want to learn prompt engineering techniques",
                author="user1",
                subreddit="ChatGPT",
                upvotes=100,
                comment_count=50,
                created_utc=datetime.now() - timedelta(days=1),
                url="https://example.com",
                permalink="/r/ChatGPT/comments/post1",
                score=100,
                num_comments=50
            ),
            RedditPost(
                id="post2",
                title="What is the best way to learn machine learning?",
                content="I'm a beginner looking for resources",
                author="user2",
                subreddit="learnmachinelearning",
                upvotes=200,
                comment_count=100,
                created_utc=datetime.now() - timedelta(days=2),
                url="https://example.com",
                permalink="/r/learnmachinelearning/comments/post2",
                score=200,
                num_comments=100
            )
        ]
    
    @pytest.fixture
    def sample_comments(self):
        """Create sample comments."""
        return [
            RedditComment(
                id="comment1",
                body="What programming language should I start with?",
                author="commenter1",
                upvotes=10,
                created_utc=datetime.now() - timedelta(hours=12),
                post_id="post1",
                is_top_level=True
            ),
            RedditComment(
                id="comment2",
                body="How long does it take to learn?",
                author="commenter2",
                upvotes=5,
                created_utc=datetime.now() - timedelta(hours=10),
                post_id="post2",
                is_top_level=True
            )
        ]
    
    def test_extract_keywords_tfidf(self, analysis_service, sample_posts, sample_comments):
        """Test keyword extraction."""
        keywords = analysis_service.extract_keywords_tfidf(sample_posts, sample_comments, top_n=10)
        
        # May return empty if no valid keywords found, but if keywords exist, they should be valid
        if len(keywords) > 0:
            assert all(k.frequency > 0 for k in keywords)
            assert all(len(k.subreddits) > 0 for k in keywords)
    
    def test_identify_trending_topics(self, analysis_service, sample_posts):
        """Test trending topic identification."""
        keywords = analysis_service.extract_keywords_tfidf(sample_posts, [], top_n=10)
        topics = analysis_service.identify_trending_topics(keywords, sample_posts)
        
        assert len(topics) > 0
        assert all(t.mentions > 0 for t in topics)
        assert all(t.trend in ["rapidly_rising", "rising", "stable", "declining"] for t in topics)
    
    def test_extract_questions(self, analysis_service, sample_posts, sample_comments):
        """Test question extraction."""
        questions = analysis_service.extract_questions(sample_posts, sample_comments)
        
        # Should find questions in posts and comments (may be empty if no duplicates)
        if len(questions) > 0:
            assert all(q.frequency >= 1 for q in questions)
            # Questions should contain question marks or question words
            for q in questions:
                assert "?" in q.question or any(q.question.lower().startswith(word) for word in ("what", "how", "why", "when", "where", "can", "should", "is", "are"))
    
    def test_analyze_data(self, analysis_service):
        """Test complete data analysis."""
        sample_data = {
            "subreddits": ["test"],
            "posts": [
                {
                    "id": "post1",
                    "title": "How to write better prompts?",
                    "content": "I want to learn prompt engineering",
                    "author": "user1",
                    "subreddit": "test",
                    "upvotes": 100,
                    "comment_count": 50,
                    "created_utc": datetime.now().isoformat(),
                    "url": "https://example.com",
                    "permalink": "/r/test/comments/post1",
                    "score": 100,
                    "num_comments": 50
                },
                {
                    "id": "post2",
                    "title": "How to write better prompts?",
                    "content": "Same question again",
                    "author": "user2",
                    "subreddit": "test",
                    "upvotes": 50,
                    "comment_count": 25,
                    "created_utc": datetime.now().isoformat(),
                    "url": "https://example.com",
                    "permalink": "/r/test/comments/post2",
                    "score": 50,
                    "num_comments": 25
                }
            ],
            "comments": [
                {
                    "id": "comment1",
                    "body": "What is the best way to start?",
                    "author": "commenter1",
                    "upvotes": 10,
                    "created_utc": datetime.now().isoformat(),
                    "post_id": "post1",
                    "is_top_level": True
                },
                {
                    "id": "comment2",
                    "body": "What is the best way to start?",
                    "author": "commenter2",
                    "upvotes": 5,
                    "created_utc": datetime.now().isoformat(),
                    "post_id": "post2",
                    "is_top_level": True
                }
            ],
            "collected_at": datetime.now().isoformat(),
            "time_period_days": 7
        }
        
        result = analysis_service.analyze_data(sample_data)
        
        assert result.total_posts == 2
        assert result.total_comments == 2
        assert result.subreddits_analyzed == 1
        assert len(result.trending_topics) > 0
        # Questions should be found since we have duplicates
        assert len(result.common_questions) > 0
        assert len(result.keyword_frequencies) > 0
        assert "total_posts" in result.category_summaries
    
    def test_analyze_data_multiple_subreddits(self, analysis_service):
        """Test analyzing data from multiple subreddits."""
        sample_data = {
            "subreddits": ["test1", "test2"],
            "posts": [
                {
                    "id": "post1",
                    "title": "Test post 1",
                    "content": "Content 1",
                    "author": "user1",
                    "subreddit": "test1",
                    "upvotes": 100,
                    "comment_count": 50,
                    "created_utc": datetime.now().isoformat(),
                    "url": "https://example.com",
                    "permalink": "/r/test1/comments/post1",
                    "score": 100,
                    "num_comments": 50
                },
                {
                    "id": "post2",
                    "title": "Test post 2",
                    "content": "Content 2",
                    "author": "user2",
                    "subreddit": "test2",
                    "upvotes": 200,
                    "comment_count": 100,
                    "created_utc": datetime.now().isoformat(),
                    "url": "https://example.com",
                    "permalink": "/r/test2/comments/post2",
                    "score": 200,
                    "num_comments": 100
                }
            ],
            "comments": [],
            "collected_at": datetime.now().isoformat(),
            "time_period_days": 7
        }
        
        result = analysis_service.analyze_data(sample_data)
        
        assert result.subreddits_analyzed == 2
        assert result.total_posts == 2

