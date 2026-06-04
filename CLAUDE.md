# CLAUDE.md — Project Memory

> This file is read automatically by Claude Code at the start of every session.
> Keep it updated as the project evolves.

---

## What this project is

**own-your-pace** is a self-hosted fitness data aggregator. It pulls activity data
from external providers (Strava) and stores it permanently on your own server —
so your fitness history is never lost if a service shuts down or you lose access.

It is NOT a Strava replacement or social fitness platform. It is a personal data
ownership tool.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 18 + TimescaleDB + PostGIS |
| Cache / Queue | Redis 7 + Celery |
| Sync orchestration | n8n |
| Frontend | React 18 + Vite |
| Reverse proxy | Nginx |
| Containers | Docker + Docker Compose |

---

## Project structure

```
backend/app/
├── api/v1/     → route handlers only, no logic
├── core/       → config, security, dependencies
├── models/     → SQLAlchemy ORM models
├── schemas/    → Pydantic request/response contracts
├── services/   → ALL business logic lives here
├── workers/    → Celery background jobs
└── db/         → session, base, Alembic migrations
```

---

## Key architectural decisions

- **Models vs Schemas are always separate** — `models/` is SQLAlchemy ORM,
  `schemas/` is Pydantic. Never mix them.
- **Business logic in services/, never in api/** — route handlers only validate,
  call a service, and return a response.
- **n8n is an external sync agent** — it does not write to DB directly.
  It calls FastAPI endpoints. All logic stays in FastAPI.
- **Deduplication via external_id** — each workout stores the provider's original
  ID. n8n checks this before posting to avoid duplicates.
- **PostGIS for routes** — GPS tracks stored as `geometry(LineString)`,
  not JSON arrays. Enables spatial queries and indexing.
- **TimescaleDB hypertables** — `workouts` (on `started_at`) and `metrics`
  (on `recorded_at`) will be converted to hypertables in Phase 3.
- **Redis dual-purpose** — both cache layer and Celery broker.

---

## Current phase

**Phase 1 — Foundation** ✅ Complete

## Progress

- [x] Phase 1 — Foundation (auth, DB, core setup)
- [ ] Phase 2 — Data Ingestion (Strava webhook, file upload, Celery workers)
- [ ] Phase 3 — API Layer (workouts, metrics, gear endpoints)
- [ ] Phase 4 — UI + Orchestration (React dashboard, n8n workflows)
- [ ] Phase 5 — Production (CI/CD, monitoring, backup)

---

## Coding conventions

- Type hints on all function signatures
- `Mapped[]` annotations for all SQLAlchemy 2.0 columns
- All config via `pydantic-settings`, never hardcoded
- Every new endpoint needs: schema + service + route (in that order)
- Commit messages follow Conventional Commits: `feat:`, `fix:`, `docs:`, etc.
- English only — all code, comments, and documentation

---

## DO NOT

- Put business logic in route handlers (`api/`)
- Hardcode any config value — use `.env` + `core/config.py`
- Mix SQLAlchemy models with Pydantic schemas
- Commit `.env` files
- Write to the database directly from n8n workflows