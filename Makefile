# Makefile for Watchlist Manager

.PHONY: help setup install start stop clean test lint format

help: ## Show this help message
	@echo "🎬 Watchlist Manager - Available Commands"
	@echo "========================================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

setup: ## Initial project setup
	@echo "🔧 Setting up Watchlist Manager..."
	./setup.sh

install: ## Install dependencies
	@echo "📦 Installing backend dependencies..."
	cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
	@echo "📦 Installing frontend dependencies..."
	cd frontend && npm install

start: ## Start development servers
	@echo "🚀 Starting development servers..."
	@echo "Backend will run on http://localhost:8000"
	@echo "Frontend will run on http://localhost:3000"
	@echo ""
	@echo "Open two terminals and run:"
	@echo "Terminal 1: make start-backend"
	@echo "Terminal 2: make start-frontend"

start-backend: ## Start backend server
	cd backend && source venv/bin/activate && uvicorn main:app --reload

start-frontend: ## Start frontend server
	cd frontend && npm start

stop: ## Stop all services
	@echo "🛑 Stopping services..."
	@pkill -f "uvicorn main:app" || true
	@pkill -f "npm start" || true

docker-up: ## Start with Docker
	docker-compose up -d

docker-down: ## Stop Docker containers
	docker-compose down

test: ## Run all tests
	@echo "🧪 Running backend tests..."
	cd backend && source venv/bin/activate && pytest tests/ -v
	@echo "🧪 Running frontend tests..."
	cd frontend && npm test -- --watchAll=false

test-backend: ## Run backend tests only
	cd backend && source venv/bin/activate && pytest tests/ -v --cov=app

test-frontend: ## Run frontend tests only
	cd frontend && npm test -- --watchAll=false

lint: ## Run linting
	@echo "🔍 Linting backend..."
	cd backend && source venv/bin/activate && flake8 app/
	@echo "🔍 Linting frontend..."
	cd frontend && npm run lint

format: ## Format code
	@echo "✨ Formatting backend code..."
	cd backend && source venv/bin/activate && black app/ && isort app/
	@echo "✨ Formatting frontend code..."
	cd frontend && npm run format

clean: ## Clean build artifacts
	@echo "🧹 Cleaning build artifacts..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	rm -rf backend/.pytest_cache || true
	rm -rf frontend/build || true
	rm -rf frontend/node_modules || true

init-db: ## Initialize database
	cd backend && source venv/bin/activate && python -c "from app.database import init_db; init_db()"

backup-db: ## Backup database
	@echo "💾 Creating database backup..."
	cp backend/watchlist.db backend/watchlist_backup_$(shell date +%Y%m%d_%H%M%S).db

dev-setup: ## Quick development setup
	@echo "⚡ Quick development setup..."
	make install
	make init-db
	@echo "✅ Ready for development!"

prod-build: ## Build for production
	@echo "🏗️ Building for production..."
	cd frontend && npm run build
	@echo "✅ Production build complete!"

# GitHub-specific commands
commit-setup: ## Setup git hooks and commit templates
	@echo "📝 Setting up git hooks..."
	cp scripts/pre-commit .git/hooks/pre-commit
	chmod +x .git/hooks/pre-commit

release: ## Create a new release
	@echo "🚀 Creating new release..."
	@read -p "Enter version (e.g., v1.0.0): " version; \
	git tag -a $$version -m "Release $$version"; \
	git push origin $$version
