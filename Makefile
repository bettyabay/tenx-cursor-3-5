.PHONY: help setup test spec-check db-migrate db-upgrade db-downgrade docker-build docker-up docker-down lint format clean install dev-install frontend-install frontend-dev frontend-build

help: ## Show this help message
	@echo "Project Chimera - Makefile Commands"
	@echo "===================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies
	@echo "Installing dependencies..."
	pip install uv
	uv pip install -r requirements.txt
	uv pip install -r requirements-test.txt
	@echo "✅ Dependencies installed"

install: setup ## Alias for setup

dev-install: setup ## Install development dependencies
	uv pip install -e ".[dev]"
	@echo "✅ Development dependencies installed"

test: ## Run tests
	@echo "Starting test database services..."
	docker-compose up -d postgres redis weaviate
	@echo "Waiting for services to be ready..."
	sleep 5
	@echo "Running tests..."
	pytest tests/ -v --tb=short
	@echo "✅ Tests completed"

test-cov: ## Run tests with coverage
	docker-compose up -d postgres redis weaviate
	sleep 5
	pytest tests/ -v --cov=src --cov-report=html --cov-report=term
	@echo "✅ Coverage report generated in htmlcov/"

spec-check: ## Verify code aligns with specs
	@echo "Checking spec alignment..."
	@if [ -f scripts/spec_checker.py ]; then \
		python scripts/spec_checker.py; \
	else \
		echo "⚠️  spec_checker.py not found. Skipping spec check."; \
		echo "   Create scripts/spec_checker.py to enable this check."; \
	fi

db-migrate: ## Run database migrations
	@echo "Running database migrations..."
	docker-compose up -d postgres
	sleep 5
	alembic upgrade head
	@echo "✅ Migrations completed"

db-upgrade: db-migrate ## Alias for db-migrate

db-downgrade: ## Rollback last migration
	@echo "Rolling back last migration..."
	alembic downgrade -1
	@echo "✅ Migration rolled back"

db-reset: ## Reset database (WARNING: Destructive)
	@echo "⚠️  WARNING: This will destroy all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		docker-compose down -v postgres; \
		docker-compose up -d postgres; \
		sleep 5; \
		alembic upgrade head; \
		echo "✅ Database reset"; \
	fi

docker-build: ## Build Docker image
	@echo "Building Docker image..."
	docker build -t project-chimera:latest .
	@echo "✅ Docker image built"

docker-up: ## Start Docker services
	@echo "Starting Docker services..."
	docker-compose up -d
	@echo "✅ Services started"

docker-down: ## Stop Docker services
	@echo "Stopping Docker services..."
	docker-compose down
	@echo "✅ Services stopped"

docker-logs: ## View Docker logs
	docker-compose logs -f

lint: ## Run linters
	@echo "Running linters..."
	@if command -v ruff > /dev/null; then \
		ruff check src/ tests/; \
	else \
		echo "⚠️  ruff not installed. Run 'make dev-install'"; \
	fi
	@if command -v mypy > /dev/null; then \
		mypy src/ --ignore-missing-imports; \
	else \
		echo "⚠️  mypy not installed. Run 'make dev-install'"; \
	fi
	@echo "✅ Linting completed"

format: ## Format code
	@echo "Formatting code..."
	@if command -v black > /dev/null; then \
		black src/ tests/; \
	else \
		echo "⚠️  black not installed. Run 'make dev-install'"; \
	fi
	@if command -v ruff > /dev/null; then \
		ruff format src/ tests/; \
	else \
		echo "⚠️  ruff not installed. Run 'make dev-install'"; \
	fi
	@echo "✅ Code formatted"

clean: ## Clean temporary files
	@echo "Cleaning temporary files..."
	find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name ".mypy_cache" -exec rm -r {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -r {} + 2>/dev/null || true
	@echo "✅ Clean completed"

frontend-install: ## Install frontend dependencies
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Frontend dependencies installed"

frontend-dev: ## Start frontend development server
	@echo "Starting frontend development server..."
	cd frontend && npm run dev

frontend-build: ## Build frontend for production
	@echo "Building frontend..."
	cd frontend && npm run build
	@echo "✅ Frontend built"

all: clean setup test lint ## Run setup, tests, and linting
	@echo "✅ All checks completed"
