# SWMRA Frontend

Citizen-facing PWA built with React, Vite, Tailwind CSS, React Router, Zustand, and Zod-powered forms.

## Getting Started
```bash
npm install
npm run dev
```
The app expects the backend at `VITE_API_BASE` (see `.env.example`).

## Available Scripts
- `npm run dev` – Vite dev server with hot reload.
- `npm run build` – Production build.
- `npm run preview` – Preview the build locally.
- `npm run test` – Vitest + React Testing Library suites.
- `npm run lint` – ESLint checks.
- `npm run format` – Prettier format helper.

## Architecture Highlights
- `src/app` – providers, router, Zustand stores.
- `src/api` – axios clients with auth interceptors.
- `src/pages` – Routed screens (login, signup, dashboard, requests lifecycle).
- `src/components` – Tailwind UI primitives.
- `src/hooks` – File upload + slot helpers.
- `src/tests` – Vitest + RTL coverage for forms.

Service workers + manifest come from `vite-plugin-pwa`, with icons located under `public/`.