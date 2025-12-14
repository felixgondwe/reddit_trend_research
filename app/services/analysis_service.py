"""Analysis services for keyword frequency, trends, and question extraction."""
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set
import logging

from app.models.domain import (
    RedditPost,
    RedditComment,
    KeywordFrequency,
    TrendingTopic,
    ExtractedQuestion,
    AnalysisResult
)

logger = logging.getLogger(__name__)


class AnalysisService:
    """Service for analyzing Reddit data."""
    
    # Question patterns
    QUESTION_PATTERNS = [
        r'^[Ww]hat\s+',
        r'^[Hh]ow\s+',
        r'^[Ww]hy\s+',
        r'^[Ww]hen\s+',
        r'^[Ww]here\s+',
        r'^[Cc]an\s+',
        r'^[Ss]hould\s+',
        r'^[Ii]s\s+',
        r'^[Aa]re\s+',
        r'\?$',  # Ends with question mark
    ]
    
    def __init__(self):
        """Initialize analysis service."""
        self.question_regex = re.compile('|'.join(self.QUESTION_PATTERNS))
    
    def extract_keywords_tfidf(
        self,
        posts: List[RedditPost],
        comments: List[RedditComment],
        top_n: int = 50
    ) -> List[KeywordFrequency]:
        """
        Extract keywords using TF-IDF approach (simplified).
        
        This is a simple frequency-based approach, not full TF-IDF,
        but serves the same purpose for trend identification.
        
        Args:
            posts: List of Reddit posts
            comments: List of Reddit comments
            top_n: Number of top keywords to return
            
        Returns:
            List of KeywordFrequency objects
        """
        # Combine all text
        all_text = []
        post_text_map = defaultdict(set)  # Track which posts contain which keywords
        
        for post in posts:
            text = f"{post.title} {post.content or ''}".lower()
            all_text.append(text)
            # Simple word extraction (split on whitespace and punctuation)
            words = re.findall(r'\b[a-z]{3,}\b', text)  # Words with 3+ letters
            for word in words:
                post_text_map[word].add(post.id)
        
        for comment in comments:
            text = comment.body.lower()
            all_text.append(text)
            words = re.findall(r'\b[a-z]{3,}\b', text)
            for word in words:
                # Find which post this comment belongs to
                for post in posts:
                    if comment.post_id == post.id:
                        post_text_map[word].add(post.id)
                        break
        
        # Count frequencies
        word_freq = Counter()
        for text in all_text:
            words = re.findall(r'\b[a-z]{3,}\b', text.lower())
            word_freq.update(words)
        
        # Filter common stop words (simplified list)
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her',
            'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 'how',
            'its', 'may', 'new', 'now', 'old', 'see', 'two', 'way', 'who', 'boy',
            'did', 'has', 'let', 'put', 'say', 'she', 'too', 'use', 'reddit', 'subreddit'
        }
        
        # Get top keywords
        keywords = []
        for word, freq in word_freq.most_common(top_n * 2):  # Get more to filter
            if word not in stop_words and len(word) > 3:
                # Find which subreddits this keyword appears in
                subreddits = set()
                post_ids = list(post_text_map[word])
                
                for post in posts:
                    if post.id in post_text_map[word]:
                        subreddits.add(post.subreddit)
                
                keywords.append(KeywordFrequency(
                    keyword=word,
                    frequency=freq,
                    subreddits=list(subreddits),
                    posts=post_ids[:10]  # Limit post references
                ))
                
                if len(keywords) >= top_n:
                    break
        
        return keywords
    
    def identify_trending_topics(
        self,
        keywords: List[KeywordFrequency],
        posts: List[RedditPost]
    ) -> List[TrendingTopic]:
        """
        Identify trending topics from keywords.
        
        Args:
            keywords: List of keyword frequencies
            posts: List of Reddit posts
            
        Returns:
            List of TrendingTopic objects
        """
        # Group keywords by topic (simplified - using keyword as topic)
        topics = []
        
        for keyword in keywords[:30]:  # Top 30 keywords
            # Find posts mentioning this keyword
            topic_posts = []
            for post in posts:
                text = f"{post.title} {post.content or ''}".lower()
                if keyword.keyword in text:
                    topic_posts.append({
                        "title": post.title,
                        "upvotes": post.upvotes,
                        "comments": post.num_comments,
                        "subreddit": post.subreddit
                        # Author and links anonymized for privacy
                    })
            
            # Determine trend (simplified - based on frequency)
            mentions = keyword.frequency
            if mentions > 50:
                trend = "rapidly_rising"
            elif mentions > 20:
                trend = "rising"
            elif mentions > 10:
                trend = "stable"
            else:
                trend = "declining"
            
            topics.append(TrendingTopic(
                topic=keyword.keyword,
                mentions=mentions,
                trend=trend,
                subreddits=keyword.subreddits,
                change_percentage=None,  # Would need historical data
                posts=topic_posts[:5]  # Top 5 posts
            ))
        
        return topics
    
    def extract_questions(
        self,
        posts: List[RedditPost],
        comments: List[RedditComment]
    ) -> List[ExtractedQuestion]:
        """
        Extract common questions using pattern matching.
        
        Args:
            posts: List of Reddit posts
            comments: List of Reddit comments
            
        Returns:
            List of ExtractedQuestion objects
        """
        questions = []
        question_texts = []
        
        # Extract questions from posts
        for post in posts:
            text = post.title
            if self.question_regex.search(text):
                question_texts.append({
                    "text": text,
                    "post": post,
                    "source": "post"
                })
        
        # Extract questions from comments
        for comment in comments:
            text = comment.body
            if self.question_regex.search(text):
                # Find the post this comment belongs to
                post = next((p for p in posts if p.id == comment.post_id), None)
                if post:
                    question_texts.append({
                        "text": text[:200],  # Limit length
                        "post": post,
                        "source": "comment"
                    })
        
        # Group similar questions
        question_groups = defaultdict(list)
        for q in question_texts:
            # Normalize question text
            normalized = q["text"].lower().strip()
            # Use first 50 chars as key for grouping
            key = normalized[:50]
            question_groups[key].append(q)
        
        # Create ExtractedQuestion objects
        for key, group in question_groups.items():
            if len(group) >= 2:  # Only questions that appear multiple times
                # Use the most common version
                question_text = group[0]["text"]
                
                # Get unique subreddits
                subreddits = list(set(q["post"].subreddit for q in group))
                
                # Get post references (anonymized)
                post_refs = []
                for q in group[:5]:  # Top 5 examples
                    post_refs.append({
                        "title": q["post"].title,
                        "upvotes": q["post"].upvotes,
                        "comments": q["post"].num_comments,
                        "subreddit": q["post"].subreddit
                        # Author and links anonymized for privacy
                    })
                
                # Calculate average engagement
                avg_upvotes = sum(q["post"].upvotes for q in group) / len(group)
                avg_comments = sum(q["post"].num_comments for q in group) / len(group)
                
                questions.append(ExtractedQuestion(
                    question=question_text,
                    frequency=len(group),
                    subreddits=subreddits,
                    posts=post_refs,
                    avg_engagement={
                        "avg_upvotes": round(avg_upvotes, 2),
                        "avg_comments": round(avg_comments, 2)
                    }
                ))
        
        # Sort by frequency
        questions.sort(key=lambda x: x.frequency, reverse=True)
        
        return questions[:20]  # Top 20 questions
    
    def analyze_data(
        self,
        subreddit_data: Dict[str, Any]
    ) -> AnalysisResult:
        """
        Perform complete analysis on collected data.
        
        Args:
            subreddit_data: Dictionary with posts and comments from collection
            
        Returns:
            AnalysisResult object
        """
        # Convert to domain models
        posts = [RedditPost(**p) for p in subreddit_data.get("posts", [])]
        comments = [RedditComment(**c) for c in subreddit_data.get("comments", [])]
        
        # Get number of subreddits analyzed
        subreddits_analyzed = len(subreddit_data.get("subreddits", [])) if "subreddits" in subreddit_data else 1
        
        # Extract keywords
        keywords = self.extract_keywords_tfidf(posts, comments)
        
        # Identify trending topics
        trending_topics = self.identify_trending_topics(keywords, posts)
        
        # Extract questions
        common_questions = self.extract_questions(posts, comments)
        
        # Group by category (if subreddits are categorized)
        category_summaries = {
            "total_posts": len(posts),
            "total_comments": len(comments),
            "subreddits_analyzed": subreddits_analyzed,
            "top_keywords": [k.keyword for k in keywords[:10]],
            "top_questions": [q.question for q in common_questions[:5]],
            "trending_topics_count": len(trending_topics),
            "common_questions_count": len(common_questions)
        }
        
        return AnalysisResult(
            analysis_date=datetime.now(),
            time_period={
                "start": (datetime.now() - timedelta(days=subreddit_data.get("time_period_days", 7))).isoformat(),
                "end": datetime.now().isoformat(),
                "days": subreddit_data.get("time_period_days", 7)
            },
            subreddits_analyzed=subreddits_analyzed,
            total_posts=len(posts),
            total_comments=len(comments),
            trending_topics=trending_topics,
            common_questions=common_questions,
            keyword_frequencies=keywords,
            category_summaries=category_summaries
        )

