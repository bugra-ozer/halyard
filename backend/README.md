# Halyard Backend

FastAPI backend service for Halyard.

## Prerequisites

- Python (managed via `.python-version`)
- [uv](https://docs.astral.sh/uv/)

## Setup

Install dependencies into a virtual environment:

```bash
uv sync
```

### Running Locally
```bash
uv run uvicorn app.main:app --reload

uv run pytest
```