# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- SQLAlchemy models: Sport, Workout, Lap, SyncSource, Gear, Metric
- Alembic autogenerate migration covering all Phase 2 tables (single clean migration)
- Updated `script.py.mako` — added `import geoalchemy2` to migration template
- Updated `env.py` — PostGIS table exclusion + all model imports

### Fixed
- GeoAlchemy2 spatial index conflict — set `spatial_index=False` on Geometry columns, let Alembic manage indexes exclusively

---

## [0.1.0-alpha] - 2026-06-04

### Added
- FastAPI project scaffold with layered architecture (api, core, models, schemas, services, workers, db)
- PostgreSQL 18 + TimescaleDB + PostGIS via Docker Compose (dev environment)
- SQLAlchemy 2.0 ORM setup with DeclarativeBase
- Alembic migration: initial users table with UUID PK, timestamps, timezone, unit preference
- JWT authentication — register, login, refresh token, `/me` endpoints
- Pydantic v2 schemas for user request/response contracts
- `pyproject.toml` with pinned dependencies for Python 3.12
- Health check endpoint (`GET /health`)
- `docker-compose.dev.yml` — infrastructure only (DB + Redis + n8n) for local development
- Initial database schema design (ERD) — users, workouts, metrics, gear, sync_sources, sports, laps
- React + Vite frontend folder scaffold
- n8n, Nginx, and scripts folder scaffold
- GitHub Actions CI workflow (lint, test, Docker build)
- Project documentation — README, CONTRIBUTING, architecture, self-hosting guides
- `CLAUDE.md` — project memory for Claude Code
- `AGENTS.md` — AI coding agent context for OpenCode, Claude Code, Cursor
- `docs/development-phases.md` — full phase breakdown with deliverables and definition of done

### Fixed
- Pinned `bcrypt==4.0.1` — passlib not compatible with bcrypt 5.x
- Changed DB host port to `5434` — port 5432 was already occupied by another PostgreSQL instance on Windows, causing auth failures on all connections to that port
- Fixed `pyproject.toml` build backend from `setuptools.backends.legacy` to `setuptools.build_meta`
- Fixed `ALLOWED_ORIGINS` parsing — pydantic-settings requires JSON array format for list fields
- Commented out unimplemented model relationships (`Workout`, `SyncSource`, `Metric`, `Gear`) to unblock FastAPI startup