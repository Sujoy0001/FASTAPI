# Server Frontend - Task Manager API

## How to Run

### Method 1: Using Batch Script (with Nginx)

```bash
.\start-with-nginx.bat
```

This starts both FastAPI and Nginx.

- Access at: `http://localhost`

### Method 2: Running FastAPI Directly

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

- Access at: `http://localhost:8000`

## Setup

1. Install dependencies:

```bash
uv sync
```

2. Activate virtual environment:

```bash
.venv\Scripts\activate
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`
- **Home**: `http://localhost:8000/api`

## Project Structure

- `app/` - Main application code
  - `main.py` - FastAPI application entry point
  - `database.py` - Database configuration
  - `models.py` - SQLAlchemy models
  - `schemas.py` - Pydantic schemas
  - `routes/` - API route handlers
- `nginx/` - Nginx configuration for reverse proxy

## Celery (Background Tasks)

This project uses Celery for background processing with Redis as the broker/back-end.

Run Redis (example using Docker):

```bash
docker run -p 6379:6379 redis:7
```

Start the Celery worker:

```bash
celery -A app.celery_app.celery_app worker --loglevel=info
```

Start the FastAPI app as usual (e.g. uvicorn):

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

When a new task is created via the API, a background job `notify_task_created` is enqueued.
