# makefile-tier: lib
.DEFAULT_GOAL := help

.PHONY: help install dev test test-cov docker-test lint format typecheck build pre-commit clean

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
		awk 'BEGIN{FS=":.*##"}{printf "  %-20s %s\n", $$1, $$2}'

install: ## Install dev dependencies + pre-commit hooks
	pip install -e ".[dev]"
	pre-commit install

dev: install ## Alias for install (no separate dev server)

test: ## Run unit tests
	pytest tests/ --tb=short

test-cov: ## Run tests with coverage
	pytest tests/ --cov=django_autoload --cov-report=term-missing --cov-report=xml

lint: ## Run ruff linter
	ruff check src tests

format: ## Auto-format code
	ruff format src tests

typecheck: ## Run mypy type checking
	mypy src/django_autoload

docker-test: ## Run tests in Docker (CI-compatible)
	@# Pre-create coverage.xml as a regular file so docker cp has a target.
	@rm -rf coverage.xml
	@touch coverage.xml
	docker build -f Dockerfile.test -t django-autoload-test .
	@# Run without --rm so we can copy coverage.xml out, then remove the container.
	docker run --name django-autoload-test-run django-autoload-test; \
	  EXIT=$$?; \
	  docker cp django-autoload-test-run:/app/coverage.xml ./coverage.xml 2>/dev/null || true; \
	  docker rm django-autoload-test-run; \
	  exit $$EXIT

build: ## Build wheel distribution package
	python -m build

pre-commit: ## Run all pre-commit checks
	pre-commit run --all-files

clean: ## Remove build artifacts
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .ruff_cache .coverage build dist *.egg-info 2>/dev/null || true
