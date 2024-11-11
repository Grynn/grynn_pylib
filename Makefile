# Makefile

.PHONY: all clean install test version

install:
	pip install -e .

clean:
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .venv
	rm -rf requirements.txt
	rm -rf .pytest_cache

test: install
	pytest

version: test
	@VERSION=$(or $(VERSION), patch)
	@NEW_VERSION=$(shell python bump_version.py $$VERSION)
