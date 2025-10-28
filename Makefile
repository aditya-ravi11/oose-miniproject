.PHONY: up down seed test fmt lint

up:
	docker compose up --build

down:
	docker compose down

seed:
	python backend/app/db/seed.py

test:
	cd backend && pytest
	cd frontend && npm run test

fmt:
	cd backend && ruff format .
	cd frontend && npm run format

lint:
	cd backend && ruff check .
	cd frontend && npm run lint
