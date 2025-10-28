# Smart Waste Management & Recycling Assistant (SWMRA)

SWMRA is a citizen-first platform that helps residents schedule waste pickups, receive updates, and earn recycling rewards. This monorepo contains the FastAPI backend, React PWA frontend, infrastructure seeds, and developer tooling required for phase one of the project.

## Features
- FastAPI backend with JWT auth, MongoDB persistence, and modular services for requests, slots, notifications, and rewards.
- Background jobs via APScheduler for draft cleanup and queued email delivery.
- Notification pipeline with SMTP email provider and feature-flagged SMS/Push stubs plus WebSocket streaming.
- React + Vite + Tailwind frontend with Zustand stores, React Hook Form + Zod validation, and PWA shell.
- Dockerized developer experience with seed data, Makefile targets, and detailed runbook.

## Getting Started
1. **Clone and configure**
   `ash
   cp .env.example .env
   # adjust secrets such as JWT_SECRET or SMTP credentials
   `
2. **Install tooling**
   - Backend: pyenv/python 3.11, poetry or pip per ackend/pyproject.toml.
   - Frontend: 
ode >= 18, 
pm or pnpm.
3. **Start services**
   `ash
   make up        # docker compose up with backend, frontend, mongo, mailhog
   make seed      # seed baseline users and slots
   `
4. **Run tests**
   `ash
   make test      # orchestrates backend pytest + frontend vitest
   `

See ARCHITECTURE.md, API.md, and RUNBOOK.md for deeper dives into design, HTTP contracts, and operational guidance.
