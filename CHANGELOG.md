# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [0.1.0-alpha] - 2025-06-01

### Added
- FastAPI project scaffold with layered architecture (api, core, models, schemas, services, workers, db)
- PostgreSQL 16 + TimescaleDB + PostGIS via Docker Compose (dev environment)
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