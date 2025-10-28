# ARCHITECTURE

## Overview
Smart Waste Management & Recycling Assistant (SWMRA) is a polyglot monorepo that ships a FastAPI backend, a React + Vite PWA frontend, and infra assets (Docker, Mongo seeds, docs). Phase 1 focuses on citizen flows: authentication, pickup requests, slots, notifications, and rewards.

## Backend
- **Framework**: FastAPI + Uvicorn running under Python 3.11.
- **Persistence**: MongoDB via Motor async client. Collections: `users`, `pickup_requests`, `notifications`, `rewards`, and placeholder `slot_templates` for seed data.
- **Structure**:
  - `core/` Settings (pydantic-settings), security/JWT/passlib, structured logging, and the rate limit middleware.
  - `db/` Motor client factory + index bootstrap.
  - `models/` Pydantic schemas for IO contracts.
  - `repositories/` Encapsulate Mongo queries per aggregate (users, requests, notifications, rewards).
  - `services/` Encapsulate business logic: auth, requests (state machine + validation), slots (capacity aware), notifications (queue + SMTP), rewards, storage, websocket hub.
  - `routers/` FastAPI routers per bounded context (auth, requests, slots, files, notifications, rewards, ws, health).
  - `workers/` APScheduler jobs for draft cleanup + notification delivery.
  - `tests/` Pytest suites with async-friendly fixtures and repo fakes.
- **Cross-cutting**:
  - JWT bearer auth using PyJWT, hashed passwords using passlib[bcrypt].
  - Rate limiting middleware (per IP requests/minute) before hitting routers.
  - File storage abstraction writing to `/uploads/<year>/<month>/<uuid>.ext` with a path ready to swap for S3 later.
  - Notification manager fans out to WebSocket clients (`/ws/notifications`) and SMTP via `smtplib`. SMS/Push stubs honor feature flags.
  - APScheduler runs in-process to clean stale drafts (older than 7 days) and drain queued email notifications every 2 minutes.
  - Reward engine grants +5 points for recyclable completion, +10 for e-waste/hazardous, storing records in `rewards`.

## Frontend
- **Framework**: React 18, Vite, TypeScript, Tailwind CSS.
- **State Management**: Lightweight Zustand stores (`auth`, `requests`, `notifications`). Auth store hydrates token from `localStorage` and wires bootstrap/me calls. Notification store opens a WebSocket and keeps unread counts.
- **Routing**: React Router DOM with guarded routes. Auth-only routes sit inside `AppLayout`, which provides nav, notification bell, and reward badge.
- **Forms & Validation**: React Hook Form + Zod for login/signup and the multi-step new request wizard. File uploads leverage a custom hook hitting `/files/upload`.
- **UI System**: Small kit of Tailwind-based components (Button, Card, EmptyState, RequestCard, Timeline, NotificationBell). Layout emphasizes mobile-friendly rounded surfaces.
- **PWA**: `vite-plugin-pwa` generates the manifest/service worker. Icons live under `frontend/public`.
- **Testing**: Vitest + React Testing Library validate critical forms (auth + new request wizard).

## Notifications & Realtime Flow
1. Domain events (request submitted, slot confirmed, completion) queue notification documents.
2. APScheduler job flushes queued notifications via SMTP (or feature-flagged stubs for SMS/Push).
3. In-app notifications flow through the WebSocket manager immediately after queueing (`channel = inapp`).
4. Frontend `useNotificationStore` opens `ws://API/ws/notifications?token=...` and updates bell counts live.

## Background Jobs
- **Draft cleanup**: nightly job removes requests stuck in `draft` older than 7 days, keeping the DB lean.
- **Notification dispatcher**: polling job grabs `notifications.status == queued` and sends via configured channels.

## Deployment Notes
- Docker Compose orchestrates MongoDB, backend, frontend, and optional Mailhog.
- `.env` at repo root drives both backend (`pydantic-settings`) and frontend (Vite `import.meta.env`).
- Pre-commit hooks (Black, isort, ESLint, Prettier) keep the codebase consistent.