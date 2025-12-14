# Setup and Installation Guide

This guide will help you set up and run the Reddit Trend Research Tool.

## Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (optional, for containerized deployment)
- Reddit API credentials (client ID and secret)

## Quick Start

### 1. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/felixgondwe/reddit_trend_research.git
cd reddit_trend_research

# Initialize project (creates .env and installs dependencies)
make init
```

### 2. Configure Reddit API

Edit the `.env` file with your Reddit API credentials:

```bash
REDDIT_CLIENT_ID=your_client_id_here
REDDIT_CLIENT_SECRET=your_client_secret_here
REDDIT_USERNAME=your_reddit_username
REDDIT_PASSWORD=your_reddit_password
REDDIT_USER_AGENT=python:reddit_trend_research:v1.0.0 (by /u/your_username)
```

### 3. Run the Application

#### Option A: Using Make (Recommended)

```bash
# Run API and Dashboard separately (in different terminals)
make run-api        # Terminal 1
make run-dashboard  # Terminal 2
```

#### Option B: Using Docker

```bash
# Build and start containers
make docker-build
make docker-up

# View logs
make docker-logs
```

#### Option C: Manual

```bash
# Terminal 1: Start FastAPI
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start Streamlit
streamlit run streamlit_app/dashboard.py --server.port 8501
```

### 4. Access the Application

- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:8501

## Usage

### Collecting Data

1. Open the Streamlit dashboard at http://localhost:8501
2. Navigate to "Data Collection" page
3. Configure collection settings:
   - Subreddits (leave empty for all 25 target subreddits)
   - Posts per subreddit (default: 100)
   - Time period (default: 7 days)
   - Include comments (default: Yes)
4. Click "Start Collection"
5. Wait for collection to complete (may take 10-30 minutes for all subreddits)

### Analyzing Data

1. After collection, go to "Analysis Results" page
2. The latest analysis will be displayed automatically
3. View trending topics and common questions

### API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check
- `POST /collect` - Collect data from Reddit
- `POST /analyze` - Analyze collected data
- `GET /data/files` - List all data files
- `GET /data/{filename}` - Get specific data file
- `GET /analysis/latest` - Get latest analysis
- `GET /subreddits` - Get target subreddits list

## Makefile Commands

```bash
make help          # Show all available commands
make install        # Install dependencies
make setup-env      # Create .env file
make run-api        # Run FastAPI server
make run-dashboard  # Run Streamlit dashboard
make docker-build   # Build Docker images
make docker-up      # Start Docker containers
make docker-down    # Stop Docker containers
make docker-logs    # View Docker logs
make test           # Run tests
make lint           # Run linter
make format         # Format code
make clean          # Clean cache files
```

## Troubleshooting

### API Connection Errors

If the dashboard can't connect to the API:
- Ensure the FastAPI server is running on port 8000
- Check that `API_BASE_URL` in `dashboard.py` matches your setup
- Verify firewall settings

### Rate Limit Errors

The tool automatically handles rate limiting:
- Maximum 60 requests per minute
- Exponential backoff on errors
- Automatic retry with delays

### Cache Issues

Clear cache if needed:
```bash
make clean-data
```

## Development

### Running Tests

```bash
make test
```

### Code Formatting

```bash
make format
make lint
```

### Project Structure

```
reddit_trend_research/
├── app/
│   ├── api/           # FastAPI endpoints
│   ├── models/        # Domain models
│   ├── services/      # Business logic
│   └── utils/         # Utilities (rate limiting, caching)
├── streamlit_app/     # Streamlit dashboard
├── tests/             # Test files
├── docs/              # Documentation
└── examples/          # Example outputs
```

## Compliance

This tool is designed to comply with Reddit's API terms:
- ✅ Read-only access
- ✅ Rate limiting (60 req/min)
- ✅ Caching (1 hour posts, 30 min comments)
- ✅ Proper attribution
- ✅ No AI/ML training
- ✅ Personal, non-commercial use

See [docs/API_COMPLIANCE.md](docs/API_COMPLIANCE.md) for details.

## Support

For issues or questions:
- Check the documentation in `docs/`
- Open an issue on GitHub
- Review [CONTRIBUTING.md](CONTRIBUTING.md)

