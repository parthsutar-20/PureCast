# ── PureCast Makefile ─────────────────────────────────────
# Usage: make <target>
# Run `make help` for a list of all targets.
# ──────────────────────────────────────────────────────────

.DEFAULT_GOAL := help
SHELL := /bin/bash
PYTHON := python
UV := uv

# Colours
CYAN := \033[36m
RESET := \033[0m

# ── Environment ──────────────────────────────────────────

.PHONY: install
install: ## Install all dependencies (dev)
	$(UV) sync --all-extras

.PHONY: install-prod
install-prod: ## Install production dependencies only
	$(UV) sync --no-dev

.PHONY: lock
lock: ## Update the lockfile
	$(UV) lock

# ── Quality ──────────────────────────────────────────────

.PHONY: lint
lint: ## Run ruff linter
	$(UV) run ruff check src/ tests/

.PHONY: lint-fix
lint-fix: ## Run ruff linter with auto-fix
	$(UV) run ruff check --fix src/ tests/

.PHONY: format
format: ## Format code with ruff
	$(UV) run ruff format src/ tests/

.PHONY: format-check
format-check: ## Check formatting without changing files
	$(UV) run ruff format --check src/ tests/

.PHONY: typecheck
typecheck: ## Run mypy strict type checking
	$(UV) run mypy src/

.PHONY: security
security: ## Run bandit security scan
	$(UV) run bandit -r src/purecast/ -c pyproject.toml

.PHONY: audit
audit: ## Audit dependencies for vulnerabilities
	$(UV) run pip-audit

.PHONY: check
check: lint format-check typecheck security ## Run all static checks

# ── Testing ──────────────────────────────────────────────

.PHONY: test
test: ## Run unit tests
	$(UV) run pytest tests/unit/ -v --tb=short

.PHONY: test-integration
test-integration: ## Run integration tests (requires Docker)
	$(UV) run pytest tests/integration/ -v --tb=short

.PHONY: test-e2e
test-e2e: ## Run end-to-end tests (requires full stack)
	$(UV) run pytest tests/e2e/ -v --tb=short

.PHONY: test-property
test-property: ## Run property-based tests
	$(UV) run pytest tests/property/ -v --tb=short

.PHONY: test-all
test-all: ## Run all tests with coverage
	$(UV) run pytest tests/ -v --tb=short --cov --cov-report=term-missing --cov-report=html

.PHONY: test-load
test-load: ## Run load tests with Locust (headless, 60s)
	$(UV) run locust -f tests/load/locustfile.py --headless -u 100 -r 10 --run-time 60s --host http://localhost:8000

.PHONY: coverage
coverage: ## Generate coverage report
	$(UV) run pytest tests/unit/ tests/property/ --cov --cov-report=html --cov-report=term-missing
	@echo "Report: htmlcov/index.html"

# ── Database ─────────────────────────────────────────────

.PHONY: db-upgrade
db-upgrade: ## Run Alembic migrations to head
	$(UV) run alembic upgrade head

.PHONY: db-downgrade
db-downgrade: ## Rollback one migration
	$(UV) run alembic downgrade -1

.PHONY: db-revision
db-revision: ## Create a new migration (MSG required)
	$(UV) run alembic revision --autogenerate -m "$(MSG)"

.PHONY: db-history
db-history: ## Show migration history
	$(UV) run alembic history --verbose

# ── Docker ───────────────────────────────────────────────

.PHONY: up
up: ## Start dev stack (docker-compose)
	docker compose up -d

.PHONY: down
down: ## Stop dev stack
	docker compose down

.PHONY: up-prod
up-prod: ## Start production stack
	docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

.PHONY: build
build: ## Build all Docker images
	docker compose build

.PHONY: logs
logs: ## Tail all container logs
	docker compose logs -f

.PHONY: ps
ps: ## Show running containers
	docker compose ps

# ── Application ──────────────────────────────────────────

.PHONY: api
api: ## Run the API server (dev mode)
	$(UV) run uvicorn purecast.main:app --reload --host 0.0.0.0 --port 8000

.PHONY: worker
worker: ## Run the ARQ worker
	$(UV) run purecast-worker

.PHONY: ingestor
ingestor: ## Run the MQTT ingestor
	$(UV) run purecast-ingestor

.PHONY: simulator
simulator: ## Run the purifier simulator
	$(UV) run purecast-simulator

# ── Scripts ──────────────────────────────────────────────

.PHONY: seed
seed: ## Seed demo data
	$(UV) run python scripts/seed_demo.py

.PHONY: create-admin
create-admin: ## Create an admin user
	$(UV) run python scripts/create_admin.py

.PHONY: openapi
openapi: ## Export OpenAPI spec to docs/openapi.json
	$(UV) run python scripts/export_openapi.py

.PHONY: evaluate
evaluate: ## Run evaluation harness
	$(UV) run python scripts/run_evaluation.py

# ── Demo ─────────────────────────────────────────────────

.PHONY: demo
demo: up seed ## Full demo: start stack, seed data, run scripted scenarios
	@echo ""
	@echo "$(CYAN)🚀 PureCast stack is running!$(RESET)"
	@echo "$(CYAN)   API:       http://localhost:8000$(RESET)"
	@echo "$(CYAN)   API Docs:  http://localhost:8000/docs$(RESET)"
	@echo "$(CYAN)   Grafana:   http://localhost:3000$(RESET)"
	@echo "$(CYAN)   MQTT:      localhost:1883$(RESET)"
	@echo ""
	@echo "$(CYAN)Running demo scenarios...$(RESET)"
	$(UV) run purecast-simulator --scenario demo

# ── Cleanup ──────────────────────────────────────────────

.PHONY: clean
clean: ## Remove build artifacts and caches
	rm -rf build/ dist/ *.egg-info .mypy_cache .pytest_cache .ruff_cache htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true

# ── Help ─────────────────────────────────────────────────

.PHONY: help
help: ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "$(CYAN)%-18s$(RESET) %s\n", $$1, $$2}'
