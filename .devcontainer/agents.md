# Devcontainer Configuration

## Overview

Minimal Python devcontainer with uv package manager and ruff for linting/formatting.

## Key Features

- **Base Image**: Python 3.12
- **Package Manager**: uv
- **Linting/Formatting**: ruff (only)
- **Virtual Environment**: Mounted as named volume to keep container .venv separate from host

## Usage

1. Open folder in VS Code
2. Reopen in Container (Command Palette: "Dev Containers: Reopen in Container")
3. Dependencies auto-install via `uv sync --all-extras`
4. Run make targets as usual

## Volume

The `.venv` directory is mounted as a Docker volume, ensuring the container's Python environment stays isolated from the host machine's .venv.
