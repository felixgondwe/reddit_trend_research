# Reddit Trend Research Tool

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

Personal research tool for staying up to date with trending discussions in AI/ML and fitness communities—the topics I care about and want to learn from.

**Repository:** https://github.com/felixgondwe/reddit_trend_research

---

## Purpose

I built this tool to stay current with what communities I care about are discussing. I'm passionate about AI trends and love fitness, so I want to make sure I'm learning about the topics these communities are actively talking about.

By analyzing discussions across 25 carefully selected subreddits in AI/ML and fitness, this tool helps me:

- **Stay up to date with AI trends** - See what AI tools, techniques, and discussions are gaining traction
- **Learn from community questions** - Understand what beginners and experts are asking about
- **Follow fitness discussions** - Track popular training methodologies, nutrition strategies, and community insights
- **Identify emerging topics** - Discover new trends and topics before they become mainstream
- **Focus my learning** - Ensure I'm spending time on topics that are currently relevant and actively discussed

This is a personal learning tool to help me stay informed about the communities I care about. It's used exclusively for personal research and learning—no commercial use, no data monetization, and no AI/ML model training.

---

## Target Communities

This tool monitors **25 subreddits** across four categories:

### AI & AI Education Communities (10)

| Subreddit | Members | Engagement Probability | Focus Area |
|-----------|---------|----------------------|------------|
| r/ChatGPT | 5.6M+ | **95%** | ChatGPT applications, prompt engineering, practical AI use cases |
| r/MachineLearning | 2.9M | **88%** | ML research, neural networks, technical discussions, research papers |
| r/artificial | 822K | **85%** | General AI, computer vision, robotics, NLP applications |
| r/learnmachinelearning | 500K+ | **90%** | Beginner-friendly ML tutorials, learning resources, educational content |
| r/OpenAI | 730K+ | **82%** | OpenAI developments, GPT models, DALL-E, latest AI innovations |
| r/ArtificialIntelligence | 1.4M | **78%** | AI news, industry trends, ethical discussions, societal impact |
| r/datascience | 817K | **80%** | Data science applications, ML implementation, career advice |
| r/deeplearning | 200K+ | **70%** | Deep learning techniques, neural networks, advanced research |
| r/LocalLLaMA | 150K+ | **83%** | Local LLM deployment, open-source models, optimization techniques |
| r/AIPromptProgramming | 69K+ | **88%** | Prompt engineering, AI programming strategies, optimization tips |

**Research Focus:** AI tool adoption, learning resources, common beginner questions, emerging techniques, educational gaps

---

### Running Communities (5)

| Subreddit | Members | Engagement Probability | Focus Area |
|-----------|---------|----------------------|------------|
| r/running | 1.2M+ | **92%** | General running discussions, training plans, gear reviews, all experience levels |
| r/AdvancedRunning | 300K+ | **85%** | Race preparation, performance optimization, advanced training techniques |
| r/RunningShoeGeeks | 150K+ | **88%** | Running shoe reviews, biomechanics analysis, detailed gear comparisons |
| r/C25K | 200K+ | **78%** | Couch to 5K program, beginner support, motivation, progress tracking |
| r/ultrarunning | 100K+ | **75%** | Ultra-distance running, extreme endurance, mental strategies, nutrition |

**Research Focus:** Training methodologies, injury prevention, nutrition strategies, gear recommendations, beginner challenges

---

### Nutrition Communities (5)

| Subreddit | Members | Engagement Probability | Focus Area |
|-----------|---------|----------------------|------------|
| r/nutrition | 2.4M+ | **90%** | Evidence-based nutrition science, macros, micronutrients, scientific debates |
| r/EatCheapAndHealthy | 3.8M+ | **93%** | Budget-friendly healthy meals, meal prep, practical nutrition advice |
| r/keto | 3.9M+ | **91%** | Ketogenic diet methodology, low-carb nutrition, weight loss outcomes |
| r/loseit | 3.9M+ | **89%** | Sustainable weight loss, calorie tracking, lifestyle changes, motivation |
| r/fitmeals | 200K+ | **82%** | Meal planning for fitness, macros, high-protein recipes, nutrition timing |

**Research Focus:** Diet strategies, meal planning approaches, nutritional science, budget-conscious eating, weight management

---

### Strength Training Communities (5)

| Subreddit | Members | Engagement Probability | Focus Area |
|-----------|---------|----------------------|------------|
| r/weightroom | 600K+ | **90%** | Intermediate+ weight training, program design, strength development |
| r/bodybuilding | 2.7M+ | **87%** | Muscle building, aesthetics, competition prep, supplement discussions |
| r/Fitness | 9.2M+ | **85%** | General fitness, workout routines, beginner questions, comprehensive guides |
| r/gainit | 300K+ | **83%** | Weight gain strategies, bulking, progressive overload, beginner muscle building |
| r/naturalbodybuilding | 200K+ | **79%** | Natural bodybuilding, drug-free training, realistic expectations, form technique |

**Research Focus:** Training program effectiveness, progressive overload strategies, supplement efficacy, form/technique, natural vs enhanced training

---

## What It Does

This tool performs the following functions:

1. **Fetches Top Posts:** Retrieves the top 100 posts from each specified subreddit within a specified time period (typically last 7 days)

2. **Analyzes Keywords:** Uses keyword frequency analysis to identify trending topics and emerging themes

3. **Identifies Common Questions:** Extracts frequently asked questions and discussion patterns to understand community needs

4. **Tracks Engagement Metrics:** Records upvote scores, comment counts, and engagement rates to identify highly relevant topics

5. **Generates Reports:** Creates CSV and JSON reports with trending topics, common questions, and engagement metrics for research analysis

6. **Provides Attribution:** All referenced posts include links to original Reddit posts and usernames for proper attribution

---

## What It Does NOT Do

This tool is designed with strict limitations to ensure compliance with Reddit's API terms and respect for the platform:

- ❌ **Does not post, comment, or vote** - Read-only access only
- ❌ **Does not use data for AI/ML model training** - User content is never used to train algorithms or neural networks
- ❌ **Does not monetize or sell data** - No commercial use, no revenue generation from Reddit data
- ❌ **Does not scrape beyond API limits** - Strictly adheres to Reddit's rate limits (60 requests/minute)
- ❌ **Does not share user data with third parties** - All data remains local and private
- ❌ **Does not run on automated schedules** - Manual execution only, no cron jobs or automated runs
- ❌ **Does not access private or deleted content** - Only public posts and comments are accessed
- ❌ **Does not collect personally identifiable information** - No email addresses, IP addresses, or private data
- ❌ **Does not modify or republish content** - Content is analyzed but never republished or modified

---

## Technical Approach

### API & Authentication
- **API:** Reddit API via PRAW (Python Reddit API Wrapper)
- **Authentication:** OAuth2 client credentials (read-only access)
- **User-Agent:** Properly formatted with tool name, version, and repository URL
- **Why PRAW (not Devvit):** This is a standalone research tool requiring local data processing, custom analysis, and external reporting. Devvit is designed for Reddit-native apps running on Reddit's platform, which is not suitable for this use case. See [docs/WHY_NOT_DEVVIT.md](docs/WHY_NOT_DEVVIT.md) for detailed explanation.

### Rate Limiting
- **Limit:** Maximum 60 requests per minute
- **Implementation:** Exponential backoff on rate limit errors
- **Respect:** Automatic pause and retry when limits are reached

### Data Handling
- **Caching:** Local storage to minimize API calls and reduce load on Reddit's servers
- **Storage:** Local CSV/JSON files only (no cloud databases)
- **Retention:** Data automatically deleted after 30 days
- **Privacy:** No personally identifiable information collected

### Execution
- **Mode:** Manual runs via command line only
- **No Automation:** No scheduled runs, no cron jobs, no background processes
- **User Control:** Each analysis run is initiated manually by the user

---

## Reddit API Compliance

**⚠️ IMPORTANT: This tool requires explicit approval from Reddit before use. Do not use until approval is granted.**

This tool is designed to fully comply with Reddit's API Terms of Service, Developer Guidelines, and [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy):

For detailed Responsible Builder Policy compliance, see [docs/RESPONSIBLE_BUILDER_COMPLIANCE.md](docs/RESPONSIBLE_BUILDER_COMPLIANCE.md).

### General Compliance:

### Non-Commercial Use ✓
- Personal research tool only
- No revenue generation from Reddit data or services
- No commercial applications or monetization
- Personal research purpose only

### Read-Only Access ✓
- Only uses read (GET) methods
- No posting, commenting, or voting functionality
- No content modification or account actions
- Respects Reddit's read-only API access

### Data Anonymization ✓
- Author usernames are not stored (anonymized for privacy)
- Post links/URLs are not stored (local use only)
- No identifying information collected
- All data stored locally for personal research

### Rate Limiting ✓
- Strict adherence to 60 requests/minute limit
- Exponential backoff on rate limit errors
- Caching to minimize API calls
- Respectful of Reddit's server resources

### Data Retention ✓
- Maximum 30-day retention period
- Automatic deletion after analysis
- Local storage only (no cloud databases)
- No long-term data storage

### Privacy Protection ✓
- No personally identifiable information collected
- No user email addresses or IP addresses
- No private messages or profile data
- Transparent data practices

### No AI/ML Training ✓
- User content is NOT used to train machine learning models
- No algorithmic training or neural network development
- Content used only for keyword analysis and trend identification
- Research and trend analysis only

For detailed compliance documentation, see [docs/API_COMPLIANCE.md](docs/API_COMPLIANCE.md).

---

## Installation & Usage

### Prerequisites
- Python 3.8 or higher
- Reddit API credentials (client ID and secret)
- Internet connection for API access

### Configuration
1. Create a Reddit application at https://www.reddit.com/prefs/apps
2. Obtain your client ID and secret
3. Configure the tool with your credentials
4. Customize subreddit lists and analysis parameters as needed

### Running Analysis
The tool is executed manually via command line. Each run:
- Fetches top posts from configured subreddits
- Analyzes keywords and trending topics
- Generates reports in CSV/JSON format
- Stores results locally for review

### Output Format
Reports include:
- Trending topics with frequency counts
- Common questions extracted from discussions
- Engagement metrics (upvotes, comments)
- Links to original posts for attribution
- Timestamp and analysis period information

For detailed usage instructions, see [docs/USAGE.md](docs/USAGE.md).

---

## Documentation

- **[API Compliance](docs/API_COMPLIANCE.md)** - Detailed Reddit API compliance documentation
- **[Responsible Builder Compliance](docs/RESPONSIBLE_BUILDER_COMPLIANCE.md)** - Reddit Responsible Builder Policy compliance
- **[Why Not Devvit](docs/WHY_NOT_DEVVIT.md)** - Explanation of why Devvit is not applicable for this tool
- **[Usage Guide](docs/USAGE.md)** - Comprehensive usage instructions and configuration
- **[Data Policy](docs/DATA_POLICY.md)** - Data collection, usage, and privacy policies
- **[Examples](docs/EXAMPLES.md)** - Detailed use case examples and scenarios
- **[Sample Output](examples/SAMPLE_OUTPUT.md)** - Example report formats and outputs

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Contact

For questions about this tool or data practices, please open an issue in the repository or contact the maintainer.

---

## Disclaimer

This is a personal learning tool to help me stay up to date with communities I care about (AI trends and fitness). It is not affiliated with Reddit Inc. and does not represent Reddit's views or opinions. All Reddit content remains the property of its original authors and Reddit Inc.
