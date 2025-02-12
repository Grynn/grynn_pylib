# Makefile

.PHONY: all clean install test version

dev:
	uv sync

lint:
	uvx ruff check

format:
	uvx ruff format
	
build: lint format
	uv build

publish: build
	uv publish

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf requirements.txt
	rm -rf .pytest_cache
	rm -rf .ruff_cache

test: dev
	uv run pytest

version: test
	# bumpversion patch, but only if working directory is clean
	git diff-index --quiet HEAD -- || (echo "Working directory not clean, aborting" && exit 1)
	uv run bump_version.py patch