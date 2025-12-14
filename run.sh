#!/bin/bash

# Startup script for Reddit Trend Research Tool

echo "🚀 Starting Reddit Trend Research Tool..."
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please edit .env with your Reddit API credentials before continuing"
    exit 1
fi

# Check if dependencies are installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt
fi

echo "✅ Dependencies installed"
echo ""
echo "Starting services..."
echo "  - API: http://localhost:8000"
echo "  - Dashboard: http://localhost:8501"
echo ""
echo "Press Ctrl+C to stop"
echo ""

# Start API in background
python -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload &
API_PID=$!

# Wait a moment for API to start
sleep 2

# Start Streamlit
streamlit run streamlit_app/dashboard.py --server.port 8501

# Cleanup on exit
kill $API_PID 2>/dev/null

