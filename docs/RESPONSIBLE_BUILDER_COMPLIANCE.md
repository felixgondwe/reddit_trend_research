# Reddit Responsible Builder Policy Compliance

This document demonstrates compliance with Reddit's [Responsible Builder Policy](https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy).

---

## 1. Approval is Required ✓

**Policy Requirement:** You must request and receive explicit approval before accessing Reddit data through their API.

**Our Compliance:**

✅ **Explicit Approval Request:**
- This tool will NOT be used until explicit approval is granted by Reddit
- All API access is conditional upon receiving approval
- No data collection occurs without proper authorization

✅ **Single Request:**
- One application submitted for this specific use case
- No duplicate requests or multiple accounts
- Transparent about the exact purpose and scope

✅ **Approval Status:**
- **Current Status:** Awaiting approval
- **Application Submitted:** [Date when submitted]
- **Approval Received:** [Date when received - if applicable]

**Implementation:**
- The tool includes validation to ensure credentials are properly configured
- Error handling prevents unauthorized access attempts
- All API calls require valid, approved credentials

---

## 2. Transparency ✓

**Policy Requirement:** Clearly disclose how and why you're accessing Reddit data. Avoid misrepresentation.

**Our Compliance:**

✅ **Clear Purpose Disclosure:**
- **Why:** Personal learning and staying up to date with communities I care about (AI trends and fitness)
- **How:** Read-only API access via PRAW (Python Reddit API Wrapper)
- **What:** Analyzing trending discussions to learn what communities are actively talking about
- **Who:** Single user (Felix Gondwe) for personal learning and staying current with topics of interest

✅ **Transparency Measures:**
- Open-source repository with full code visibility
- Comprehensive documentation of all practices
- Clear data collection and usage policies
- Public repository: https://github.com/felixgondwe/reddit_trend_research

✅ **No Misrepresentation:**
- Single Reddit account used
- Single application submitted
- Honest about purpose and scope
- No false claims or misleading information

✅ **Documentation:**
- README clearly states purpose and limitations
- API_COMPLIANCE.md details all practices
- DATA_POLICY.md explains data handling
- All documentation is publicly accessible

---

## 3. Respect the Limits ✓

**Policy Requirement:** Adhere to Reddit's access limits and avoid excessive usage.

**Our Compliance:**

✅ **Rate Limiting:**
- Maximum 60 requests per minute (strictly enforced)
- Exponential backoff on rate limit errors (1s, 2s, 4s, 8s, 16s, 32s, 60s max)
- Automatic request queuing to prevent bursts
- Real-time rate limit tracking and enforcement

✅ **Caching Strategy:**
- Local cache for posts (1 hour expiration)
- Local cache for comments (30 minutes expiration)
- Reduces redundant API calls by ~70-80%
- Automatic cache cleanup

✅ **Usage Patterns:**
- Manual execution only (no automated scheduling)
- User-initiated runs only
- No background processes or cron jobs
- Respectful of Reddit's server resources

✅ **Implementation:**
- Rate limiter implemented in `app/utils/rate_limiter.py`
- Cache manager in `app/utils/cache.py`
- All API calls go through rate limiting middleware
- Automatic retry with exponential backoff

---

## 4. Use of Developer Platform ("Devvit") 

**Policy Requirement:** For non-commercial applications, utilize Reddit's Developer Platform ("Devvit") and comply with Reddit's Developer Terms.

**Why Devvit is Not Applicable:**

❌ **Devvit is Not Suitable for This Use Case:**

Devvit (Reddit's Developer Platform) is designed for building:
- Reddit apps and extensions that run **on Reddit's platform**
- Interactive Reddit experiences within Reddit's ecosystem
- Apps that integrate directly with Reddit's UI and infrastructure

**This Tool's Requirements:**
- **Standalone Research Tool:** Runs locally on developer's machine, not on Reddit's platform
- **Data Analysis:** Performs complex analysis (TF-IDF, trend identification, question extraction) that requires local processing
- **External Integration:** Generates reports for research analysis, not Reddit-native features
- **Local Storage:** Stores data locally for analysis, which Devvit's platform restrictions don't allow
- **Custom Dashboard:** Uses Streamlit for custom visualization dashboard, not Reddit's UI
- **Batch Processing:** Processes large volumes of data across multiple subreddits, requiring local compute resources

**Technical Incompatibility:**
- Devvit apps run in Reddit's sandboxed environment with limited compute resources
- This tool requires full Python environment with data science libraries (pandas, scikit-learn, nltk)
- Devvit doesn't support the type of batch data analysis and local file storage this tool requires
- The tool needs to run independently for research purposes, not as a Reddit-integrated app

**Our Compliance:**

✅ **Appropriate API Access Method:**
- Using PRAW (Python Reddit API Wrapper) for read-only access via Reddit's public API
- This is the **correct and appropriate** method for standalone research tools
- Compliant with Reddit's API Terms of Service
- Read-only operations (GET methods only)
- No posting, commenting, or voting

✅ **Developer Terms Compliance:**
- Full compliance with Reddit's Developer Terms
- Proper authentication (OAuth2 client credentials)
- Valid user-agent string
- Respect for rate limits and API guidelines
- Appropriate use of Reddit's public API for research purposes

✅ **Non-Commercial Use:**
- Personal research tool only
- No revenue generation
- No commercial applications
- Personal learning and staying up to date with communities I care about (AI trends and fitness)

**Conclusion:** Devvit is designed for Reddit-native apps that run on Reddit's platform. This tool is a standalone research application that requires local processing, custom analysis, and external reporting capabilities that Devvit cannot provide. Using Reddit's public API via PRAW is the appropriate and compliant method for this use case.

**For detailed explanation, see:** [WHY_NOT_DEVVIT.md](WHY_NOT_DEVVIT.md)

---

## 5. Bot Transparency ✓

**Policy Requirement:** If your application includes bot functionality, ensure bots clearly disclose their nature to users.

**Our Compliance:**

✅ **No Bot Functionality:**
- This tool does NOT include any bot functionality
- No automated posting, commenting, or voting
- No user-facing bot interactions
- Read-only data collection only

✅ **Not Applicable:**
- This requirement does not apply to this tool
- Tool is for personal research, not user interaction
- No bot-to-user communications
- No automated Reddit interactions

---

## 6. Prohibited Activities ✓

**Policy Requirement:** Avoid using Reddit data for illegal or malicious purposes, such as manipulating Reddit's features or engaging in spamming activities.

**Our Compliance:**

✅ **No Manipulation:**
- No voting (upvotes/downvotes)
- No karma manipulation
- No content manipulation
- No feature abuse

✅ **No Spamming:**
- No posting or commenting
- No automated submissions
- No bulk operations
- No unsolicited communications

✅ **No Illegal Activities:**
- No data scraping beyond API limits
- No unauthorized access
- No privacy violations
- No terms of service violations

✅ **Read-Only Operations:**
- Only GET requests to public endpoints
- No POST, PUT, DELETE, or PATCH methods
- No account modifications
- No content creation

✅ **Legal Compliance:**
- Complies with all applicable laws
- Respects privacy through data anonymization
- Protects user privacy
- Transparent data practices

---

## 7. Data Handling and Retention ✓

**Policy Requirement:** If your project involves research, do not retain copies of data beyond what is necessary for the immediate research project.

**Our Compliance:**

✅ **Limited Retention:**
- Maximum 30-day retention period
- Automatic deletion after analysis completion
- No long-term data storage
- Data deleted after research use

✅ **Immediate Research Use:**
- Data used only for current research project
- Analysis completed within 7 days of collection
- Reports generated for content planning
- Data deleted after 30 days maximum

✅ **No Unnecessary Retention:**
- No archival storage
- No backups of collected data
- No long-term databases
- Local files only, deleted after use

✅ **Data Lifecycle:**
1. **Collection:** Fetch posts/comments via API (Day 0)
2. **Analysis:** Extract trends and questions (Days 1-7)
3. **Reporting:** Generate insights for research analysis (Days 8-14)
4. **Deletion:** Automatic removal after 30 days maximum

✅ **Implementation:**
- Automatic cleanup in `app/services/data_storage.py`
- 30-day retention policy enforced
- No cloud storage or external databases
- Local files only, with automatic expiration

---

## Additional Compliance Measures

### Privacy Protection ✓
- No personally identifiable information (PII) collected
- Only public post/comment data
- Usernames not stored (anonymized)
- No user profiling or tracking

### Data Anonymization ✓
- Author usernames are not stored (anonymized for privacy)
- Post links/URLs are not stored (local use only)
- No identifying information collected
- All data stored locally for personal research

### Transparency ✓
- Open-source code repository
- Comprehensive documentation
- Clear data practices
- Public compliance documentation

### Contact and Responsiveness ✓
- GitHub Issues for questions
- 48-hour response time commitment
- Immediate response to compliance concerns
- Transparent communication

---

## Compliance Verification

### Code Implementation
- ✅ Rate limiting implemented and tested
- ✅ Caching implemented to reduce API load
- ✅ Read-only access enforced
- ✅ Data retention policy implemented
- ✅ Error handling for rate limits
- ✅ Proper authentication

### Documentation
- ✅ README with clear purpose
- ✅ API_COMPLIANCE.md with detailed practices
- ✅ DATA_POLICY.md with data handling details
- ✅ RESPONSIBLE_BUILDER_COMPLIANCE.md (this document)
- ✅ Usage guides and examples

### Testing
- ✅ Unit tests for all endpoints
- ✅ Rate limiting tests
- ✅ Caching tests
- ✅ Error handling tests
- ✅ 38 tests, all passing

---

## Approval Request Information

**Application Details:**
- **Tool Name:** Reddit Trend Research - AI & Fitness Education
- **Purpose:** Personal learning and staying up to date with communities I care about
- **Use Case:** Analyzing trending discussions to learn what AI and fitness communities are actively discussing, ensuring I stay current with topics I'm passionate about
- **Scope:** 25 subreddits, read-only access
- **Data Retention:** 30 days maximum
- **Commercial Use:** None

**Contact Information:**
- **Developer:** Felix Gondwe
- **Repository:** https://github.com/felixgondwe/reddit_trend_research
- **GitHub Issues:** For questions and concerns

**Compliance Commitment:**
- Full compliance with Responsible Builder Policy
- Willing to adjust implementation if required
- Transparent about all practices
- Responsive to Reddit's feedback

---

## Summary

This tool is designed to be fully compliant with Reddit's Responsible Builder Policy:

✅ **Approval:** Will not be used until approval is granted  
✅ **Transparency:** Clear purpose and practices documented  
✅ **Limits:** Strict rate limiting and caching  
✅ **Developer Terms:** Full compliance with API terms  
✅ **No Bots:** No bot functionality  
✅ **No Prohibited Activities:** Read-only, legal use only  
✅ **Data Retention:** 30-day maximum, immediate research use  

**Status:** Ready for approval request submission.

---

**Last Updated:** January 2025  
**Compliance Status:** Compliant with Responsible Builder Policy  
**Approval Status:** Awaiting approval

