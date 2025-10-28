# SWMRA Backend

FastAPI + MongoDB service powering authentication, pickup requests, notifications, slots, and rewards.

## Local Dev
```bash
pip install -e .[dev]
uvicorn app.main:app --reload
```

Set environment via `.env` (see repo root). Mongo indexes initialize automatically on startup.

## Tests
```bash
pytest
```

## Structure
- `app/core`: settings, security, logging, rate limiting
- `app/db`: mongo client, indexes
- `app/models`: Pydantic schemas for API IO
- `app/repositories`: data access abstractions
- `app/services`: business logic (auth, requests, notifications, rewards, slots, storage)
- `app/routers`: FastAPI routers grouped by domain
- `app/workers`: APScheduler jobs / background tasks
- `app/tests`: pytest suites (unit + API)