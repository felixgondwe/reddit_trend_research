# Quick Start Guide

Get up and running with the Reddit Trend Research Tool in 5 minutes!

## Prerequisites

- Python 3.8+
- Reddit API credentials

## Step 1: Setup Environment

```bash
# Clone and navigate to project
cd reddit_trend_research

# Create .env file from template
cp .env.template .env

# Edit .env with your Reddit API credentials
# REDDIT_CLIENT_ID=your_client_id
# REDDIT_CLIENT_SECRET=your_client_secret
# REDDIT_USERNAME=your_username
# REDDIT_PASSWORD=your_password
```

## Step 2: Install Dependencies

```bash
# Using pip
pip install -r requirements.txt

# Or using make
make install
```

## Step 3: Run the Application

### Option A: Using Make (Easiest)

```bash
# Terminal 1: Start API
make run-api

# Terminal 2: Start Dashboard
make run-dashboard
```

### Option B: Using Docker

```bash
# Build and start
make docker-build
make docker-up

# View logs
make docker-logs
```

### Option C: Using Startup Script

```bash
./run.sh
```

## Step 4: Access the Application

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

## Step 5: Collect Data

1. Open dashboard: http://localhost:8501
2. Go to "Data Collection" page
3. Click "Start Collection" (uses default settings)
4. Wait for collection to complete (~10-30 min for all subreddits)

## Step 6: View Results

1. Go to "Analysis Results" page
2. View trending topics and common questions
3. Explore "Trending Topics" and "Common Questions" pages

## API Usage Example

```bash
# Collect data via API
curl -X POST "http://localhost:8000/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "posts_per_subreddit": 50,
    "time_period_days": 7
  }'

# Get latest analysis
curl "http://localhost:8000/analysis/latest"
```

## Troubleshooting

**API not connecting?**
- Check API is running: `curl http://localhost:8000/health`
- Verify port 8000 is available

**Rate limit errors?**
- Normal! Tool handles automatically with exponential backoff
- Collection may take longer if rate limited

**Need help?**
- Check [README_SETUP.md](README_SETUP.md) for detailed setup
- Review [docs/USAGE.md](docs/USAGE.md) for usage guide

## Next Steps

- Customize subreddit lists in `app/config.py`
- Adjust analysis parameters in `.env`
- Explore API endpoints at http://localhost:8000/docs
- Review compliance docs in `docs/API_COMPLIANCE.md`

---

**That's it! You're ready to research Reddit trends! 🚀**

