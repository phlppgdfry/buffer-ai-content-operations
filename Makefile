.PHONY: help install test lint format clean run-demo

help:
	@echo "Available commands:"
	@echo "  make install    - Install package in editable mode with dev dependencies"
	@echo "  make test       - Run pytest test suite"
	@echo "  make lint       - Run ruff linter check"
	@echo "  make format     - Format code with ruff"
	@echo "  make clean      - Clean cache and build artifacts"
	@echo "  make run-demo   - Run pipeline demo in dry-run mode"

install:
	uv pip install -e ".[dev]"

test:
	pytest -v

lint:
	ruff check .

format:
	ruff format .

clean:
	rm -rf .pytest_cache .ruff_cache build dist *.egg-info

run-demo:
	python3 -m buffer_content_ops.cli demo --dry-run
