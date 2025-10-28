# RUNBOOK

## Prerequisites
- Docker + Docker Compose v2
- Python 3.11+
- Node.js 20+
- Make (optional but encouraged)

## Environment
1. Copy the example env: `cp .env.example .env`
2. Adjust secrets (JWT, SMTP credentials, feature flags, slot capacity, etc.).

## Starting the Stack
```bash
make up          # builds images and starts mongo, backend, frontend, mailhog
```
- Backend: http://localhost:8000 (FastAPI docs at `/docs`).
- Frontend: http://localhost:5173
- Mongo: exposed on `localhost:27017` for Compass or mongosh.
- Mailhog (optional): http://localhost:8025 captures outbound SMTP.

## Seeding Data
```bash
make seed        # runs python -m app.scripts.seed
```
- Inserts sample citizen user(s) from `infra/seed/seed_users.json` if not present.
- Loads illustrative slot templates into `slot_templates` (future use).

## Running Locally Without Docker
```bash
cd backend && pip install -e .[dev] && uvicorn app.main:app --reload
cd frontend && npm install && npm run dev
```
Ensure MongoDB is running locally (adjust `MONGO_URI` accordingly).

## Tests & Lint
```bash
make test-backend      # pytest (async-friendly)
make test-frontend     # vitest + RTL
make fmt-backend
make fmt-frontend
```
Pre-commit hooks (`.pre-commit-config.yaml`) enforce Black + isort (Python) and ESLint + Prettier (frontend). Install via `pre-commit install`.

## Background Jobs / Scheduler
- APScheduler fires on API startup (see `app/workers/scheduler.py`).
- Jobs run inside the FastAPI process; logs stream to stdout.
- If you disable the scheduler (e.g., unit tests), call `init_scheduler()` manually when ready.

## File Uploads
- Stored under `/uploads` relative to repo root (mounted inside the backend container).
- Served via FastAPI `StaticFiles` at `/uploads/...`.
- For production, implement a new adapter inside `StorageService` to push to S3 and update `STORAGE_BASE_URL`.

## SMTP Troubleshooting
- Default `.env` points to Mailtrap. Swap to Mailhog by setting `SMTP_HOST=mailhog` & `SMTP_PORT=1025`.
- Check logs under `backend` container or Mailhog UI if messages are missing.

## Logs & Monitoring
- Backend logs: `docker compose logs backend -f`
- Scheduler jobs log to the same stream with structured prefixes.
- Frontend logs: `docker compose logs frontend -f`
- Mongo shell: `docker exec -it <mongo-container> mongosh`.

## Failure Modes
- **401s everywhere**: ensure `swmra_token` is present; otherwise re-login. The frontend listens for `swmra:unauthorized` events to auto-logout.
- **Uploads failing**: confirm `/uploads` directory exists and container user can write (Compose mounts host folder automatically).
- **SMTP timeouts**: check credentials; in dev aim at Mailhog/Mailtrap.
- **WebSocket disconnects**: ensure you pass a valid JWT token query param. The server closes the socket with code `4001` if the token cannot be decoded.

## Production Considerations
- Move scheduler jobs into a dedicated worker (Celery/Redis) when scaling beyond a single replica.
- Replace in-memory rate limiter with Redis for horizontal scaling.
- Swap local storage & SMTP stubs for S3 and Twilio when infra is ready.
- Harden JWT secret + rotation, enforce HTTPS, and front the API with a reverse proxy that terminates TLS.