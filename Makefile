# AI Standards Training System - Makefile

.PHONY: help install setup test clean run-api run-web process train compare demo docker-build docker-run

# Default target
help:
	@echo "AI Standards Training System - Available Commands:"
	@echo ""
	@echo "Setup Commands:"
	@echo "  setup          - Setup environment and create .env file"
	@echo "  install        - Install all dependencies"
	@echo "  git-setup      - Setup Git repository with proper configuration"
	@echo "  fix-deps       - Fix dependency conflicts"
	@echo "  resolve-deps   - Resolve dependencies using alternative packages"
	@echo ""
	@echo "Processing Commands:"
	@echo "  process        - Process PDFs in base/ folder"
	@echo "  auto-process   - Automated processing (recommended)"
	@echo "  train          - Train AI models from processed data"
	@echo "  compare        - Compare two standards (requires --standard-a and --standard-b)"
	@echo "  demo           - Run complete demo"
	@echo ""
	@echo "Run Commands:"
	@echo "  run-api        - Start FastAPI server"
	@echo "  run-web        - Start Streamlit web interface"
	@echo ""
	@echo "Testing Commands:"
	@echo "  test           - Run installation test"
	@echo "  test-extract   - Test PDF extraction"
	@echo "  evaluate       - Evaluate lighting reports against standards"
	@echo "  demo-evaluation - Demo lighting evaluation system"
	@echo ""
	@echo "Docker Commands:"
	@echo "  docker-build   - Build Docker image"
	@echo "  docker-run     - Run with Docker Compose"
	@echo ""
	@echo "Maintenance Commands:"
	@echo "  clean          - Clean temporary files and caches"
	@echo "  clean-models   - Clean trained models"
	@echo "  clean-data     - Clean processed data"

# Setup commands
setup:
	python scripts/setup_environment.py

install:
	python scripts/install.py

git-setup:
	python scripts/setup_git.py

fix-deps:
	python scripts/fix_dependencies.py

resolve-deps:
	python scripts/resolve_dependencies.py

# Processing commands
process:
	python main.py process

auto-process:
	python auto_process.py

train:
	python main.py train

compare:
	@echo "Usage: make compare standard-a=file1.pdf standard-b=file2.pdf"
	@if [ -z "$(standard-a)" ] || [ -z "$(standard-b)" ]; then \
		echo "Error: Please specify both standard-a and standard-b"; \
		exit 1; \
	fi
	python main.py compare --standard-a "$(standard-a)" --standard-b "$(standard-b)"

demo:
	python main.py demo

# Run commands
run-api:
	python main.py api

run-web:
	python main.py web

# Testing commands
test:
	python tests/test_installation.py

evaluate:
	python simple_lighting_evaluator.py

demo-evaluation:
	python demo_lighting_evaluation.py

test-extract:
	python examples/table_extraction_demo.py

# Docker commands
docker-build:
	docker build -t ai-standards .

docker-run:
	docker-compose up -d

docker-stop:
	docker-compose down

docker-logs:
	docker-compose logs -f

# Maintenance commands
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type f -name "*.log" -delete
	find . -type f -name "*.tmp" -delete
	find . -type f -name "*.temp" -delete

clean-models:
	rm -rf models/*

clean-data:
	rm -rf data/* uploads/* outputs/*

clean-all: clean clean-models clean-data

# Development commands
dev-install:
	pip install -r requirements.txt
	python -m spacy download en_core_web_sm
	python -m spacy download de_core_news_sm
	python -m spacy download fr_core_news_sm

dev-setup: setup dev-install

# Production commands
prod-build:
	docker build -t ai-standards:latest .

prod-deploy:
	docker-compose -f docker-compose.yml up -d

# Backup commands
backup:
	mkdir -p backups
	tar -czf backups/ai-standards-$(shell date +%Y%m%d_%H%M%S).tar.gz data/ models/ uploads/ outputs/ --exclude="*.log"

# Status commands
status:
	@echo "System Status:"
	@echo "=============="
	@echo "Python version: $(shell python --version 2>/dev/null || echo 'Not found')"
	@echo "PDF files in base/: $(shell ls base/*.pdf 2>/dev/null | wc -l || echo '0')"
	@echo "Processed files: $(shell ls uploads/*_processed.json 2>/dev/null | wc -l || echo '0')"
	@echo "Trained models: $(shell ls models/ 2>/dev/null | wc -l || echo '0')"
	@echo "Log files: $(shell ls logs/*.log 2>/dev/null | wc -l || echo '0')"

