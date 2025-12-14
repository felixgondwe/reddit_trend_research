# Data Policy

This document outlines how the Reddit Trend Research Tool collects, uses, stores, and protects data.

---

## Data Collection

### What Data is Collected

This tool collects the following **public** data from Reddit:

#### Post Data
- **Post titles** - The title of Reddit posts
- **Post content** - The text content of self-posts (if applicable)
- **Post URLs** - Links to external content (for reference only)
- **Post timestamps** - When the post was created
- **Upvote scores** - Number of upvotes (public metric)
- **Comment counts** - Number of comments (public metric)
- **Subreddit names** - Which subreddit the post belongs to
- **Post IDs** - Reddit's unique identifier for the post

#### Comment Data
- **Comment text** - The text content of top-level comments
- **Comment upvote scores** - Number of upvotes on comments
- **Comment timestamps** - When the comment was created
- **Comment IDs** - Reddit's unique identifier for the comment

#### Author Information
- **Author usernames** - NOT stored (anonymized for privacy)
- **No author data** - No usernames, profiles, history, or personal information collected

#### Metadata
- **Subreddit information** - Public subreddit names and descriptions
- **Engagement metrics** - Public upvote and comment counts
- **Time-based data** - Post and comment timestamps

### What Data is NOT Collected

This tool explicitly **does NOT** collect:

- ❌ **User email addresses** - No email collection
- ❌ **IP addresses** - No network information
- ❌ **Private messages** - No access to private communications
- ❌ **Deleted content** - Only active, public content
- ❌ **User profiles** - No profile data collected
- ❌ **Author usernames** - Not stored (anonymized)
- ❌ **Voting history** - No individual voting records
- ❌ **Account information** - No account details or settings
- ❌ **Location data** - No geographic information
- ❌ **Device information** - No device or browser data
- ❌ **Cookies or tracking data** - No tracking mechanisms
- ❌ **Private subreddit content** - Only public subreddits
- ❌ **Removed or banned content** - Only visible, public content

---

## Data Usage

### How Data is Used

Collected data is used **exclusively** for:

#### 1. Keyword Analysis
- **Frequency counting** - Count how often keywords appear
- **Trend identification** - Identify rising or declining topics
- **Topic extraction** - Extract main themes from discussions
- **Statistical analysis** - Simple frequency and pattern analysis

#### 2. Question Extraction
- **Pattern matching** - Identify question patterns in text
- **Common question identification** - Find frequently asked questions
- **Context analysis** - Understand what questions are being asked
- **Gap identification** - Find topics with unanswered questions

#### 3. Engagement Analysis
- **Metric tracking** - Track upvote and comment counts
- **Popularity identification** - Identify highly engaging content
- **Trend correlation** - Correlate topics with engagement levels
- **Relevance scoring** - Score topics by community interest

#### 4. Research Analysis
- **Topic validation** - Validate if topics are currently relevant
- **Gap identification** - Find areas of interest and knowledge gaps
- **Trend tracking** - Track how topics evolve over time
- **Community need assessment** - Understand what communities are discussing

### How Data is NOT Used

Collected data is **explicitly NOT** used for:

- ❌ **AI/ML model training** - No training of algorithms or neural networks
- ❌ **Selling or monetization** - No commercial use or data sales
- ❌ **Third-party sharing** - No sharing with external parties
- ❌ **Automated decision making** - No automated systems using the data
- ❌ **Advertising or marketing** - No advertising or marketing purposes
- ❌ **User profiling** - No individual user profiling or tracking
- ❌ **Behavioral analysis** - No analysis of individual user behavior
- ❌ **Content recommendation** - No recommendation system development
- ❌ **Surveillance or monitoring** - No surveillance of users or communities
- ❌ **Data aggregation services** - No aggregation for external services

---

## Data Storage

### Storage Location

- **Local storage only** - All data stored on local machine
- **No cloud databases** - No cloud storage services used
- **No external services** - No third-party storage providers
- **No backups** - No backup copies created

### Storage Format

Data is stored in:
- **CSV files** - Structured data in comma-separated format
- **JSON files** - Structured data in JSON format
- **Text files** - Summary reports in plain text

### Storage Security

- **File system encryption** - Relies on operating system encryption
- **No unencrypted transmission** - All API communication uses HTTPS
- **Access control** - Files stored with appropriate permissions
- **No public access** - Files not accessible via web or network

### Data Retention

- **Maximum retention: 30 days** - Data automatically deleted after 30 days
- **Automatic deletion** - Cleanup process removes old data
- **No long-term storage** - No archival or permanent storage
- **Immediate deletion available** - Manual deletion possible at any time

### Data Lifecycle

1. **Collection** (Day 0)
   - Data fetched from Reddit API
   - Stored locally in temporary files

2. **Analysis** (Days 1-7)
   - Data analyzed for trends and insights
   - Reports generated from analysis

3. **Review** (Days 8-30)
   - Reports available for research analysis
   - Data available for reference

4. **Deletion** (Day 30+)
   - Automatic deletion after 30 days
   - All collected data removed
   - Only aggregated insights retained (if any)

---

## Data Sharing

### No Third-Party Sharing

- **No data sharing** - Data never shared with third parties
- **No API access** - No external APIs receive the data
- **No data sales** - Data never sold or licensed
- **No partnerships** - No data sharing partnerships

### Data Anonymization in Reports

Since this tool runs locally for personal research:

- **No links stored** - Post URLs/links are not stored
- **No usernames stored** - Author information is anonymized
- **Local use only** - Data never leaves the local environment
- **Privacy first** - Only post titles, content, and metrics stored

### Public Reports

Any research outputs (local only):

- **Aggregated insights only** - Only aggregated trends and patterns
- **No individual posts** - Individual posts not shared
- **Anonymized data** - No author information or links stored
- **Privacy respected** - No personal or identifying information included

---

## User Rights

### Data Access

Users whose content is analyzed have the right to:

- **Request information** - Ask what data was collected about their posts
- **Review data** - See what data is stored (if within retention period)
- **Understand usage** - Understand how their data is being used

### Data Deletion

Users can request:

- **Immediate deletion** - Request deletion of their content from stored data
- **No questions asked** - Deletion requests honored immediately
- **Confirmation** - Receive confirmation when data is deleted
- **Complete removal** - All references to their content removed

### How to Request Deletion

To request data deletion:

1. **Identify your content** - Provide post/comment IDs (if available)
2. **Contact method** - Open a GitHub issue or contact the maintainer
3. **Request deletion** - Clearly state deletion request
4. **Confirmation** - Receive confirmation within 48 hours

### Transparency

Users have the right to:

- **Understand practices** - Clear documentation of all data practices
- **Ask questions** - Contact for clarification on data handling
- **Review policy** - Access this policy document at any time
- **Report concerns** - Report any concerns about data handling

---

## Privacy Protection

### Personally Identifiable Information (PII)

- **No PII collection** - No personally identifiable information collected
- **No usernames** - Author usernames are not stored (anonymized)
- **No cross-referencing** - No linking with other data sources
- **No profiling** - No individual user profiling

### Data Minimization

- **Only necessary data** - Only collect data needed for analysis
- **Public data only** - Only access publicly available content
- **Limited scope** - Only analyze specified subreddits
- **Time-limited** - Only recent posts (last 7-30 days)

### Security Measures

- **Local storage** - Data stored locally, not in cloud
- **No network exposure** - Data not exposed to network
- **Encrypted communication** - All API communication encrypted (HTTPS)
- **Access control** - Files protected by file system permissions

---

## Compliance

### Reddit API Terms

This data policy ensures compliance with:
- Reddit API Terms of Service
- Reddit Privacy Policy
- Reddit Developer Guidelines
- General data protection principles

### Legal Compliance

- **No legal violations** - All practices comply with applicable laws
- **Respect for privacy** - Data anonymization and local storage only
- **Privacy respect** - Respect for user privacy and data rights
- **Transparency** - Clear and transparent data practices

---

## Policy Updates

### Notification of Changes

If this policy is updated:
- **Version tracking** - Policy version will be updated
- **Change log** - Significant changes will be documented
- **Repository updates** - Updated policy available in repository
- **Last updated date** - Date of last update clearly marked

### Current Version

- **Version:** 1.0
- **Last Updated:** January 2025
- **Effective Date:** January 2025

---

## Contact

For questions about data practices:

- **GitHub Issues:** https://github.com/felixgondwe/reddit_trend_research/issues
- **Repository:** https://github.com/felixgondwe/reddit_trend_research

---

## Commitment

This tool is committed to:
- **Transparent data practices** - Clear about what is collected and why
- **Minimal data collection** - Only collect what is necessary
- **Respect for privacy** - Protect user privacy and data
- **Responsible use** - Use data only for stated purposes
- **User rights** - Honor user requests and rights
- **Compliance** - Full compliance with Reddit's terms and applicable laws

---

**This policy demonstrates our commitment to responsible data handling and respect for Reddit users and their content.**

