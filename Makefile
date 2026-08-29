.PHONY: help dev up down build test lint seed train clean

help:
	@echo "PulsePredict AI - Command Center"
	@echo "--------------------------------"
	@echo "make dev       - Start backend, frontend, and redis for local development"
	@echo "make up        - Start full application stack with Docker Compose"
	@echo "make down      - Stop all Docker containers"
	@echo "make build     - Rebuild Docker images"
	@echo "make train     - Execute ML model training pipeline"
	@echo "make seed      - Populate database with comprehensive clinical & patient demo data"
	@echo "make test      - Run backend, ML engine, and frontend unit/integration test suites"
	@echo "make clean     - Clean temporary build artifacts, caches, and test runs"

dev:
	docker compose up -d postgres redis
	@echo "PostgreSQL & Redis running. Run backend and frontend locally."

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

train:
	python ml_engine/training/train_all.py

seed:
	python backend/scripts/seed_db.py

test:
	pytest backend/tests ml_engine/tests -v

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	rm -rf backend/.coverage ml_engine/.coverage frontend/.next
