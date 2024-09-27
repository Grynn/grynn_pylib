# Makefile

.PHONY: all clean install test

all: install requirements.txt

install: poetry.lock requirements.txt
	poetry install

requirements.txt: poetry.lock
	poetry export -f requirements.txt --without-hashes --output requirements.txt

poetry.lock: pyproject.toml
	poetry lock
	
clean:
	rm -rf .pytest_cache
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	rm -rf .venv
	rm requirements.txt

test:
	poetry run pytest
