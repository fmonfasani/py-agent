# Makefile for py-agent-client development

.PHONY: help install install-dev test test-cov lint format type-check clean build upload-test upload docs serve-docs

# Default target
help:
	@echo "Available commands:"
	@echo "  install      Install package in development mode"
	@echo "  install-dev  Install with development dependencies"
	@echo "  test         Run tests"
	@echo "  test-cov     Run tests with coverage report"
	@echo "  lint         Run linting checks"
	@echo "  format       Format code with black and isort"
	@echo "  type-check   Run mypy type checking"
	@echo "  clean        Clean build artifacts"
	@echo "  build        Build package"
	@echo "  upload-test  Upload to test PyPI"
	@echo "  upload       Upload to PyPI"
	@echo "  docs         Generate documentation"
	@echo "  serve-docs   Serve documentation locally"

# Installation
install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"
	pre-commit install

# Testing
test:
	pytest

test-cov:
	pytest --cov=py_agent_client --cov-report=html --cov-report=term-missing

test-integration:
	pytest tests/integration/ -v

# Code quality
lint:
	flake8 py_agent_client tests
	black --check py_agent_client tests
	isort --check-only py_agent_client tests

format:
	black py_agent_client tests
	isort py_agent_client tests

type-check:
	mypy py_agent_client

# Security
security:
	safety check
	bandit -r py_agent_client

# Cleaning
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf htmlcov/
	rm -rf .coverage
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Building and uploading
build: clean
	python -m build

upload-test: build
	python -m twine upload --repository testpypi dist/*

upload: build
	python -m twine upload dist/*

# Documentation
docs:
	mkdocs build

serve-docs:
	mkdocs serve

# Development workflow
dev-setup: install-dev
	@echo "Development environment setup complete!"
	@echo "Run 'make test' to verify everything works"

# Pre-commit hooks
pre-commit:
	pre-commit run --all-files

# CI simulation
ci: lint type-check security test-cov
	@echo "All CI checks passed!"

# Release workflow
release-check: ci build
	python -m twine check dist/*
	@echo "Release ready!"

# Examples
run-examples:
	python examples/basic_usage.py
	python examples/advanced_usage.py

# Version management
bump-patch:
	bump2version patch

bump-minor:
	bump2version minor

bump-major:
	bump2version major