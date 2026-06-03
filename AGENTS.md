# AGENTS.md — AI Coding Agent Context

> This file is read by AI coding agents (OpenCode, Claude Code, Cursor, Copilot, etc.)
> at the start of every session. Keep it updated as the project evolves.

---

## Project Identity

**Name:** own-your-pace
**Tagline:** Self-hosted fitness data aggregator. Sync once, own forever.
**Repo:** https://github.com/farhanhl-ds/own-your-pace
**Language:** Python 3.12 (backend), TypeScript (frontend)

---

## What this project does

Pulls fitness activity data from external providers (currently Strava) and stores
it permanently in a self-hosted PostgreSQL database. Users own their data — it
never disappears if a third-party service shuts down or an account is lost.

This is NOT a Strava clone, social platform, or fitness coaching app.

---

## Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Backend framework | FastAPI | 0.111.0 |
| Language | Python | 3.12 |
| ORM | SQLAlchemy | 2.0.30 |
| Migrations | Alembic | 1.13.1 |
| Database | PostgreSQL | 16 |
| Time-series | TimescaleDB | pg16-latest |
| Geospatial | PostGIS | bundled with TimescaleDB-HA |
| Geospatial ORM | GeoAlchemy2 | 0.15.1 |
| Cache / Queue | Redis | 7 |
| Background jobs | Celery | 5.4.0 |
| Sync orchestration | n8n | latest |
| Auth | python-jose + passlib | JWT / bcrypt |
| Validation | Pydantic v2 | 2.7.1 |
| Settings | pydantic-settings | 2.2.1 |
| Frontend | React 18 + Vite | - |
| Reverse proxy | Nginx | alpine |

---

## Project Structure

```
own-your-pace/
├── backend/
│   ├── app/
│   │   ├── api/v1/         ← route handlers ONLY — no business logic here
│   │   │   ├── auth.py
│   │   │   ├── users.py
│   │   │   ├── workouts.py
│   │   │   ├── metrics.py
│   │   │   ├── gear.py
│   │   │   └── sync.py
│   │   ├── core/
│   │   │   ├── config.py       ← pydantic-settings, reads from .env
│   │   │   ├── security.py     ← JWT encode/decode, bcrypt
│   │   │   ├── dependencies.py ← FastAPI Depends() — get_current_user, get_db
│   │   │   └── exceptions.py
│   │   ├── models/         ← SQLAlchemy ORM models ONLY
│   │   │   ├── user.py
│   │   │   ├── workout.py
│   │   │   ├── metric.py
│   │   │   ├── gear.py
│   │   │   ├── sync_source.py
│   │   │   └── sport.py
│   │   ├── schemas/        ← Pydantic request/response contracts ONLY
│   │   │   ├── user.py
│   │   │   ├── workout.py
│   │   │   ├── metric.py
│   │   │   ├── gear.py
│   │   │   ├── sync.py
│   │   │   └── common.py
│   │   ├── services/       ← ALL business logic lives here
│   │   │   ├── workout_service.py
│   │   │   ├── gpx_parser.py
│   │   │   ├── sync_service.py
│   │   │   ├── geo_service.py
│   │   │   └── file_processor.py
│   │   ├── workers/        ← Celery background jobs
│   │   │   ├── celery_app.py
│   │   │   ├── gpx_processor.py
│   │   │   ├── strava_sync.py
│   │   │   └── notification.py
│   │   ├── db/
│   │   │   ├── session.py      ← engine, SessionLocal, get_db()
│   │   │   ├── base.py         ← DeclarativeBase
│   │   │   └── migrations/     ← Alembic versioned migrations
│   │   └── main.py             ← FastAPI app entry point
│   └── tests/
│       ├── unit/               ← test services in isolation, mock DB
│       └── integration/        ← test full request/response cycle
├── frontend/                   ← React + Vite SPA
├── n8n/workflows/              ← n8n workflow JSON exports
├── nginx/                      ← reverse proxy config
├── docs/                       ← architecture, API reference, self-hosting
└── scripts/                    ← setup, backup, restore, migrate
```

---

## Strict Rules — Always Follow

### Architecture
- **Route handlers** (`api/`) only: validate input, call one service, return response
- **Services** (`services/`) own all business logic — validation, dedup, transforms
- **Models** (`models/`) are SQLAlchemy ORM only — never import Pydantic here
- **Schemas** (`schemas/`) are Pydantic only — never import SQLAlchemy here
- **n8n** communicates with FastAPI via HTTP + internal API key — never direct DB access
- **Config** always via `core/config.py` (pydantic-settings) — never hardcoded values

### Async Task Boundaries
Two async systems exist in this stack. Their responsibilities are strictly separated:

| Concern | n8n | Celery |
|---|---|---|
| OAuth token refresh (Strava, etc.) | ✅ | ❌ |
| Scheduled polling external providers | ✅ | ❌ |
| Strava webhook forwarding | ✅ | ❌ |
| Payload transform (provider → FastAPI) | ✅ | ❌ |
| Retry on failed external requests | ✅ | ❌ |
| Error notifications (email, Telegram) | ✅ | ❌ |
| GPX/FIT/TCX file parsing | ❌ | ✅ |
| Route geometry processing | ❌ | ✅ |
| Batch activity sync (internal) | ❌ | ✅ |
| User notifications (in-app) | ❌ | ✅ |

**Rule:** n8n owns everything between external providers and FastAPI.
Celery owns everything triggered from within the system.
Never add business logic to n8n workflows — transform only, validate in FastAPI.

### Code Style
- Type hints on ALL function signatures
- `Mapped[]` annotations on all SQLAlchemy 2.0 columns
- f-strings over `.format()`
- English only — code, comments, docstrings, commit messages
- Line length: 88 (ruff default)
- Docstrings on all service methods

### Database
- All tables: UUID primary key, `created_at`, `updated_at`
- GPS tracks stored as `geometry(LineString, 4326)` — never JSON arrays
- `workouts.external_id` used for deduplication — always check before insert
- New time-series tables → consider TimescaleDB hypertable

### Testing
- New endpoint → needs schema + service + route (in that order)
- Every endpoint needs: happy path, auth failure (401), validation failure (422)
- Unit tests mock the DB — use factory-boy for fixtures
- Integration tests use a real test DB

### Git
- Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`
- Never commit `.env` files
- Update `CHANGELOG.md` and `README.md` roadmap at end of each phase

---

## Environment Variables

All config is loaded from `.env` via `backend/app/core/config.py`.
See `.env.example` for all required variables.

Key variables:
- `DATABASE_URL` — PostgreSQL connection string
- `REDIS_URL` — Redis connection string
- `SECRET_KEY` — JWT signing key (min 32 chars)
- `STRAVA_CLIENT_ID` / `STRAVA_CLIENT_SECRET` — Strava OAuth app credentials
- `INTERNAL_API_KEY` — used by n8n to authenticate against FastAPI sync endpoints

---

## Current Development State

**Current phase:** Phase 2 — Data Ingestion (in progress)

| Phase | Status | Description |
|---|---|---|
| Phase 1 | ✅ Done | Foundation — FastAPI, DB, auth |
| Phase 2 | 🔄 Active | Strava webhook, file upload, Celery |
| Phase 3 | ⏳ Pending | API layer — workouts, metrics, gear |
| Phase 4 | ⏳ Pending | React UI + n8n workflows |
| Phase 5 | ⏳ Pending | Production — CI/CD, monitoring, docs |

---

## Running Locally

```bash
# Start infrastructure (DB + Redis + n8n)
docker compose -f docker-compose.dev.yml up -d

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload

# API docs available at:
# http://localhost:8000/api/docs
```

---

## Key Contacts & References

- Strava API docs: https://developers.strava.com/docs/reference/
- TimescaleDB docs: https://docs.timescale.com
- PostGIS docs: https://postgis.net/documentation/
- n8n docs: https://docs.n8n.io
- FastAPI docs: https://fastapi.tiangolo.com