# Reddit API Compliance Documentation

**⚠️ IMPORTANT: This tool requires explicit approval from Reddit before use. Approval must be requested and received before accessing Reddit's API.**

This document provides detailed information about how this tool complies with Reddit's API Terms of Service, Developer Guidelines, and [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).

For Responsible Builder Policy compliance details, see [RESPONSIBLE_BUILDER_COMPLIANCE.md](RESPONSIBLE_BUILDER_COMPLIANCE.md).

---

## Compliance Checklist

### Non-Commercial Use ✓

This tool is for **personal research only**. No revenue is generated from:
- Reddit data or services
- User content
- API access
- Tool outputs

**Purpose:** Personal learning and staying up to date with communities I care about. I'm passionate about AI trends and love fitness, so I use this tool to learn what these communities are actively discussing and ensure I'm staying current with relevant topics.

**Verification:** This tool has no monetization features, no subscription model, no data sales, and no commercial applications.

---

### Read-Only Access ✓

This tool only uses read (GET) methods:
- Fetching posts and comments
- Retrieving subreddit information
- Accessing public discussion data

**What it does NOT do:**
- No posting, commenting, or voting
- No content modification
- No account actions
- No private message access
- No user profile modifications

**API Methods Used:**
- `GET /api/v1/me` - Verify authentication only
- `GET /r/{subreddit}/hot` - Fetch top posts
- `GET /r/{subreddit}/comments/{article}` - Fetch comments (top-level only)
- No POST, PUT, DELETE, or PATCH methods

---

### No AI/ML Training ✓

User content is **NOT** used to:
- Train machine learning models
- Develop AI systems
- Feed into neural networks
- Any algorithmic training
- Create language models
- Build recommendation systems

User content is **ONLY** used for:
- Keyword frequency analysis (TF-IDF)
- Trend identification (simple statistical analysis)
- Question extraction (pattern matching)
- Research analysis and trend identification (manual review)

**Data Processing:**
- Simple text analysis only
- No model training or learning algorithms
- No data fed into external AI services
- No content used for training datasets

---

### Rate Limiting Implementation ✓

**Strategy:**
- Maximum 60 requests per minute (Reddit's limit)
- Exponential backoff on rate limit errors
- Request queuing to prevent bursts
- Caching to minimize redundant API calls

**Implementation Details:**
- Automatic pause when rate limit reached
- Exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s, 60s max
- Respects `X-Ratelimit-Remaining` headers
- Tracks request timestamps to prevent exceeding limits

**Caching Strategy:**
- Local cache for recently fetched posts
- Cache expiration: 1 hour for posts, 30 minutes for comments
- Reduces API load by avoiding duplicate requests
- Cache cleared after each analysis run

---

### Data Anonymization ✓

**Privacy Protection:**
Since this tool runs locally and is for personal research only:
- **Author usernames are not stored** - All author information is anonymized
- **Links to posts are not stored** - No permalinks or URLs saved
- **No identifying information** - Only post titles, content, and engagement metrics
- **Local use only** - Data never leaves the local environment

**What is Stored:**
- Post titles and content (for analysis)
- Engagement metrics (upvotes, comments)
- Subreddit names
- Timestamps (for trend analysis)
- Post IDs (for deduplication only)

**What is NOT Stored:**
- Author usernames
- Post permalinks or URLs
- Any identifying information
- User profiles or account data

---

### Data Retention and Deletion Policy ✓

**Retention Period:**
- Maximum 30 days from collection date
- Automatic deletion after analysis completion
- No long-term storage of user content

**Storage:**
- Local files only (CSV/JSON)
- No cloud databases
- No external storage services
- Encrypted at rest (file system encryption)

**Deletion Process:**
- Automatic cleanup after 30 days
- Manual deletion available on request
- No backups or archives
- Complete removal of all collected data

**Data Lifecycle:**
1. Collection: Posts fetched via API
2. Analysis: Keyword extraction and trend identification (1-7 days)
3. Reporting: Generate insights for research analysis (1-2 days)
4. Deletion: Automatic removal after 30 days maximum

---

### Privacy Protection Measures ✓

**What is Collected:**
- Post titles and content (public only)
- Comment text (top comments, public only)
- Upvote scores (public metrics)
- Comment counts (public metrics)
- Post timestamps (public metadata)
- Subreddit names (public information)

**What is NOT Collected (Anonymized):**
- Author usernames (not stored)
- Post permalinks/URLs (not stored)
- Any identifying information

**What is NOT Collected:**
- User email addresses
- IP addresses
- Private messages
- Deleted content
- User profiles beyond username
- Voting history
- Account information
- Location data
- Device information

**Privacy Safeguards:**
- No personally identifiable information (PII) collection
- Author usernames are not stored (anonymized)
- No tracking or profiling of individual users
- No cross-referencing with other data sources
- No data sharing with third parties
- All data stored locally only

---

### User-Agent Formatting ✓

**Format:**
```
User-Agent: <platform>:<app ID>:<version string> (by /u/<reddit username>)
```

**Example:**
```
User-Agent: python:reddit_trend_research:v1.0.0 (by /u/felixgondwe)
```

**Requirements:**
- Unique identifier for the application
- Version number included
- Reddit username of developer included
- Descriptive and accurate
- Updated when tool version changes

---

### Contact Information ✓

**For Questions About:**
- API compliance
- Data practices
- Tool functionality
- Reddit API usage

**Contact Methods:**
- GitHub Issues: https://github.com/felixgondwe/reddit_trend_research/issues
- Repository: https://github.com/felixgondwe/reddit_trend_research

**Response Time:**
- Issues responded to within 48 hours
- Compliance questions prioritized
- Data deletion requests honored immediately

---

## Reddit Developer Terms Compliance

### Section 1: API Access ✓
- ✅ Proper authentication via OAuth2 (client credentials)
- ✅ Valid user-agent string
- ✅ Respect for rate limits
- ✅ Read-only access only
- ✅ Using PRAW (appropriate for standalone research tools)
- ✅ Devvit not applicable (tool requires local processing and external reporting)

### Section 2: Use Restrictions ✓
- ✅ No commercial use
- ✅ No data monetization
- ✅ No AI/ML training
- ✅ Personal research only

### Section 3: Privacy & Anonymization ✓
- ✅ Author usernames not stored (anonymized)
- ✅ Post links not stored (local use only)
- ✅ No identifying information collected

### Section 4: Privacy ✓
- ✅ No PII collection
- ✅ Transparent data practices
- ✅ Limited data retention
- ✅ No third-party sharing

### Section 5: Rate Limiting ✓
- ✅ 60 requests/minute maximum
- ✅ Exponential backoff implementation
- ✅ Caching to reduce load
- ✅ Respectful of server resources

---

## Compliance Monitoring

This tool is designed to maintain compliance through:

1. **Code Review:** Regular review of API usage patterns
2. **Documentation:** Clear documentation of all practices
3. **Transparency:** Open repository with visible compliance measures
4. **Responsiveness:** Quick response to any compliance concerns
5. **Updates:** Regular updates to maintain compliance with Reddit's evolving terms

---

## Reporting Compliance Issues

If you identify any compliance concerns:

1. Open an issue in the repository
2. Clearly describe the concern
3. Provide relevant details or evidence
4. Allow 48 hours for response

All compliance issues will be addressed promptly and transparently.

---

## Compliance Commitment

This tool is committed to:
- Full compliance with Reddit's API Terms of Service
- Respect for Reddit's platform and community
- Transparent and ethical data practices
- Continuous monitoring and improvement
- Responsive handling of compliance concerns

---

**Last Updated:** January 2025  
**Compliance Status:** Active and Current

