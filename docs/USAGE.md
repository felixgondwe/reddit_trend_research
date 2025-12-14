# Usage Guide

This guide provides comprehensive instructions for using the Reddit Trend Research Tool.

---

## Getting Started

### Prerequisites

Before using this tool, ensure you have:

1. **Python 3.8 or higher** installed on your system
2. **Reddit API credentials** (client ID and secret)
3. **Internet connection** for API access
4. **Basic command-line knowledge** for running the tool

### Reddit API Credentials Setup

1. **Create a Reddit Account** (if you don't have one)
   - Visit https://www.reddit.com/register
   - Complete the registration process

2. **Create a Reddit Application**
   - Go to https://www.reddit.com/prefs/apps
   - Click "create another app..." or "create app"
   - Fill in the application details:
     - **Name:** "Reddit Trend Research - AI & Fitness Education"
     - **Type:** Select "script"
     - **Description:** Use the description from the README
     - **Redirect URI:** `http://localhost:8080`
   - Click "create app"

3. **Save Your Credentials**
   - **Client ID:** The string under your app name (looks like: `abc123def456`)
   - **Client Secret:** The "secret" field (looks like: `xyz789_secret_key`)
   - Store these securely - you'll need them for configuration

---

## Configuration

### Basic Configuration

The tool requires configuration of:

1. **API Credentials**
   - Client ID
   - Client Secret
   - Reddit username
   - Reddit password (for OAuth2)

2. **Subreddit Lists**
   - Default: All 25 target subreddits
   - Customizable: Add or remove subreddits as needed
   - Categories: AI/ML, Running, Nutrition, Strength Training

3. **Analysis Parameters**
   - Time period (default: last 7 days)
   - Number of posts per subreddit (default: 100)
   - Keyword analysis depth
   - Question extraction patterns

### Configuration File Structure

Configuration is typically stored in a local file (e.g., `config.json` or `.env`):

```json
{
  "reddit": {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "username": "your_reddit_username",
    "password": "your_reddit_password",
    "user_agent": "python:reddit_trend_research:v1.0.0 (by /u/your_username)"
  },
  "subreddits": {
    "ai_ml": [
      "ChatGPT",
      "MachineLearning",
      "artificial",
      "learnmachinelearning",
      "OpenAI",
      "ArtificialIntelligence",
      "datascience",
      "deeplearning",
      "LocalLLaMA",
      "AIPromptProgramming"
    ],
    "running": [
      "running",
      "AdvancedRunning",
      "RunningShoeGeeks",
      "C25K",
      "ultrarunning"
    ],
    "nutrition": [
      "nutrition",
      "EatCheapAndHealthy",
      "keto",
      "loseit",
      "fitmeals"
    ],
    "strength_training": [
      "weightroom",
      "bodybuilding",
      "Fitness",
      "gainit",
      "naturalbodybuilding"
    ]
  },
  "analysis": {
    "time_period_days": 7,
    "posts_per_subreddit": 100,
    "top_comments_limit": 10
  }
}
```

---

## Running Analysis

### Manual Execution

The tool is designed for **manual execution only** - no automated scheduling:

1. **Navigate to Project Directory**
   ```bash
   cd /path/to/reddit_trend_research
   ```

2. **Run the Analysis**
   ```bash
   python run_analysis.py
   ```
   (Note: This is a conceptual example - actual command may vary)

3. **Wait for Completion**
   - Progress indicators show current status
   - Rate limiting is handled automatically
   - Analysis typically takes 10-30 minutes depending on subreddit count

### Execution Process

The tool follows this process:

1. **Authentication:** Connect to Reddit API using OAuth2
2. **Subreddit Iteration:** Process each configured subreddit
3. **Post Fetching:** Retrieve top posts within time period
4. **Comment Fetching:** Get top comments for each post
5. **Analysis:** Extract keywords, identify trends, find questions
6. **Report Generation:** Create CSV/JSON reports
7. **Cleanup:** Cache cleanup and temporary file removal

### Output Locations

Reports are saved to:
- **CSV Reports:** `reports/trends_YYYY-MM-DD.csv`
- **JSON Reports:** `reports/trends_YYYY-MM-DD.json`
- **Summary:** `reports/summary_YYYY-MM-DD.txt`

---

## Understanding Results

### Report Structure

Reports contain several sections:

#### 1. Trending Topics
- **Topic:** Identified keyword or theme
- **Frequency:** Number of mentions across posts
- **Trend:** Rising (↑), Stable (→), or Declining (↓)
- **Subreddits:** Where the topic appeared

#### 2. Common Questions
- **Question:** Extracted question text
- **Frequency:** How many times similar questions appeared
- **Context:** Subreddit and post where found
- **Link:** Direct link to original post

#### 3. Engagement Metrics
- **Post Title:** Original post title
- **Upvotes:** Number of upvotes
- **Comments:** Number of comments
- **Engagement Rate:** Calculated engagement score
- **Link:** Link to original Reddit post

#### 4. Category Summaries
- **AI/ML Trends:** Top trends in AI communities
- **Running Trends:** Popular topics in running communities
- **Nutrition Trends:** Current nutrition discussions
- **Strength Training Trends:** Trending fitness topics

### Interpreting Results

**High Frequency Topics:**
- Topics mentioned frequently are likely important to the community
- Rising trends (↑) indicate growing interest
- Multiple subreddit mentions suggest broad relevance

**Common Questions:**
- Questions that appear repeatedly indicate knowledge gaps
- Beginner questions suggest areas of interest
- Technical questions indicate advanced topic interest

**Engagement Metrics:**
- High upvote counts indicate community interest
- High comment counts suggest active discussion
- Both together indicate highly relevant topics

### Using Insights for Research

1. **Identify Knowledge Gaps**
   - Look for frequently asked questions with few quality answers
   - Find topics with high engagement but limited discussion

2. **Validate Research Topics**
   - Check if topics are currently trending
   - Verify community interest and engagement

3. **Understand Community Needs**
   - See what beginners are struggling with
   - Identify advanced topics gaining traction

4. **Track Trends Over Time**
   - Compare reports from different time periods
   - Identify emerging topics early

---

## Troubleshooting

### Common Issues

#### Rate Limit Errors

**Symptom:** Error messages about rate limiting

**Solution:**
- The tool automatically handles rate limits with exponential backoff
- Wait for automatic retry (usually 1-5 minutes)
- Reduce number of subreddits if consistently hitting limits
- Increase cache duration to reduce API calls

#### Authentication Failures

**Symptom:** "Invalid credentials" or "Authentication failed"

**Solution:**
- Verify client ID and secret are correct
- Check username and password are accurate
- Ensure Reddit account is active and not restricted
- Verify user-agent string is properly formatted
- Check if Reddit API is experiencing issues

#### Network Connectivity Issues

**Symptom:** Connection timeouts or network errors

**Solution:**
- Check internet connection
- Verify Reddit API is accessible (visit reddit.com)
- Check firewall settings
- Try again after a few minutes
- Use VPN if Reddit is blocked in your region

#### Missing Data in Reports

**Symptom:** Reports show fewer posts than expected

**Solution:**
- Check if subreddits are accessible (not private or banned)
- Verify time period settings (posts may be older than expected)
- Check if subreddit has enough posts in the time period
- Review API response for errors

#### Slow Performance

**Symptom:** Analysis takes very long to complete

**Solution:**
- This is normal for 25 subreddits (10-30 minutes expected)
- Rate limiting causes intentional delays
- Reduce number of subreddits for faster runs
- Reduce posts per subreddit limit
- Check if caching is working properly

### Getting Help

If you encounter issues not covered here:

1. **Check Documentation**
   - Review [API_COMPLIANCE.md](API_COMPLIANCE.md)
   - Review [DATA_POLICY.md](DATA_POLICY.md)
   - Check [EXAMPLES.md](EXAMPLES.md) for use cases

2. **Review Error Messages**
   - Error messages usually indicate the problem
   - Check Reddit API status page
   - Verify your API credentials

3. **Open an Issue**
   - Create a GitHub issue with:
     - Description of the problem
     - Error messages (if any)
     - Steps to reproduce
     - Your configuration (without credentials)

---

## Best Practices

### Efficient Usage

1. **Use Caching**
   - Enable caching to reduce API calls
   - Cache reduces load on Reddit's servers
   - Speeds up subsequent runs

2. **Batch Analysis**
   - Run analysis for all subreddits at once
   - More efficient than individual runs
   - Better for identifying cross-community trends

3. **Regular Updates**
   - Run analysis weekly for best results
   - Track trends over time
   - Identify emerging topics early

4. **Selective Analysis**
   - Focus on specific categories when needed
   - Reduce subreddit count for faster runs
   - Customize based on current research needs

### Respectful API Usage

1. **Manual Execution Only**
   - Never automate or schedule runs
   - Always initiate manually
   - Respect Reddit's resources

2. **Rate Limit Awareness**
   - Understand rate limits (60 requests/minute)
   - Don't attempt to bypass limits
   - Use caching to minimize calls

3. **Data Retention**
   - Delete old data after 30 days
   - Don't accumulate unnecessary data
   - Follow data retention policy

---

## Advanced Configuration

### Custom Subreddit Lists

You can customize which subreddits to analyze:

- **Add Subreddits:** Include additional communities
- **Remove Subreddits:** Focus on specific categories
- **Category-Specific:** Run analysis for one category only

### Analysis Parameters

Customize analysis depth:

- **Time Period:** Adjust days to analyze (1-30 days)
- **Post Limit:** Change number of posts per subreddit (10-100)
- **Comment Depth:** Adjust how many comments to analyze
- **Keyword Threshold:** Set minimum frequency for trends

### Output Customization

Configure report formats:

- **CSV Format:** Customize column structure
- **JSON Format:** Adjust data structure
- **Summary Format:** Change summary detail level
- **Output Location:** Specify custom report directory

---

## Next Steps

After running your first analysis:

1. **Review Reports:** Examine trending topics and questions
2. **Identify Opportunities:** Find knowledge gaps and trending topics
3. **Research Analysis:** Use insights for research and trend analysis
4. **Track Trends:** Run regular analyses to track changes
5. **Refine Approach:** Adjust configuration based on results

For detailed use case examples, see [EXAMPLES.md](EXAMPLES.md).

