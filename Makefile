.PHONY: help install run-api run-dashboard run-all docker-build docker-up docker-down docker-logs clean test lint format

# Variables
PYTHON := python3
PIP := pip3
DOCKER_COMPOSE := docker-compose

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install Python dependencies
	$(PIP) install -r requirements.txt
	@echo "✅ Dependencies installed"

install-dev: ## Install development dependencies
	$(PIP) install -r requirements.txt
	$(PIP) install black flake8 pytest pytest-asyncio
	@echo "✅ Development dependencies installed"

setup-env: ## Create .env file from example
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file from .env.example"; \
		echo "⚠️  Please edit .env with your Reddit API credentials"; \
	else \
		echo "⚠️  .env file already exists"; \
	fi

run-api: ## Run FastAPI server
	$(PYTHON) -m uvicorn app.api.main:app --host 0.0.0.0 --port 8000 --reload

run-dashboard: ## Run Streamlit dashboard
	streamlit run streamlit_app/dashboard.py --server.port 8501

run-all: ## Run both API and dashboard (requires two terminals)
	@echo "Starting API and Dashboard..."
	@echo "API will run on http://localhost:8000"
	@echo "Dashboard will run on http://localhost:8501"
	@echo "Press Ctrl+C to stop"
	$(MAKE) -j2 run-api run-dashboard

docker-build: ## Build Docker images
	$(DOCKER_COMPOSE) build
	@echo "✅ Docker images built"

docker-up: ## Start Docker containers
	$(DOCKER_COMPOSE) up -d
	@echo "✅ Containers started"
	@echo "API: http://localhost:8000"
	@echo "Dashboard: http://localhost:8501"

docker-down: ## Stop Docker containers
	$(DOCKER_COMPOSE) down
	@echo "✅ Containers stopped"

docker-logs: ## Show Docker container logs
	$(DOCKER_COMPOSE) logs -f

docker-restart: ## Restart Docker containers
	$(DOCKER_COMPOSE) restart
	@echo "✅ Containers restarted"

docker-clean: ## Remove Docker containers and volumes
	$(DOCKER_COMPOSE) down -v
	@echo "✅ Docker containers and volumes removed"

test: ## Run tests
	pytest tests/ -v

lint: ## Run linter
	flake8 app/ streamlit_app/ tests/ --max-line-length=100 --exclude=__pycache__

format: ## Format code with black
	black app/ streamlit_app/ tests/ --line-length=100

clean: ## Clean cache and temporary files
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	@echo "✅ Cleaned cache and temporary files"

clean-data: ## Clean collected data and reports (use with caution)
	rm -rf app/data/cache/*.json
	rm -rf app/data/reports/*.json
	@echo "✅ Cleaned data files"

clean-all: clean clean-data ## Clean everything including data
	@echo "✅ Cleaned everything"

init: setup-env install ## Initialize project (setup env and install deps)
	@echo "✅ Project initialized"
	@echo "⚠️  Don't forget to edit .env with your Reddit API credentials"

.DEFAULT_GOAL := help

