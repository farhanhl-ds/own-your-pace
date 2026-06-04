# Development Phases

This document outlines the development roadmap for **own-your-pace**, broken into 5 phases following a bottom-up approach — infrastructure first, UI last.

---

## Overview

| Phase | Name | Status | Description |
|---|---|---|---|
| 1 | Foundation | ✅ Done | Core framework, database, authentication |
| 2 | Data Ingestion | 🔄 Active | Strava sync, file upload, background workers |
| 3 | API Layer | ⏳ Pending | REST endpoints for all resources |
| 4 | UI + Orchestration | ⏳ Pending | React dashboard, n8n workflows |
| 5 | Production | ⏳ Pending | CI/CD, monitoring, backup, deployment |

Each phase builds on the previous. Do not start a phase until the previous one is fully complete and committed.

---

## Phase 1 — Foundation

**Goal:** Get the core infrastructure running with a working authentication system.

**Deliverables:**
- FastAPI project scaffold with layered architecture
- PostgreSQL 18 + TimescaleDB + PostGIS via Docker Compose
- SQLAlchemy 2.0 ORM with DeclarativeBase
- Alembic migration setup + initial `users` table
- JWT authentication — register, login, refresh token, `/me`
- Pydantic v2 schemas for user contracts
- Health check endpoint
- Development environment (docker-compose.dev.yml)
- Project documentation — README, CONTRIBUTING, CHANGELOG, AGENTS, CLAUDE

**Definition of Done:**
- [x] `docker compose -f docker-compose.dev.yml up -d` starts all infrastructure
- [x] `alembic upgrade head` runs without errors
- [x] `POST /api/v1/auth/register` creates a user and returns 201
- [x] `POST /api/v1/auth/login` returns a valid JWT token
- [x] `GET /api/v1/auth/me` returns user data with valid token

**Status:** ✅ Complete — `v0.1.0-alpha`

---

## Phase 2 — Data Ingestion

**Goal:** Get fitness data into the database — both from Strava via webhook and from manual file uploads.

**Deliverables:**
- SQLAlchemy models: `Workout`, `Sport`, `Lap`, `SyncSource`, `Gear`
- Alembic migrations for all new tables
- Strava OAuth2 flow — connect account, store and refresh tokens
- Strava webhook endpoint — receive and process activity events
- Manual file upload endpoint — accept GPX, FIT, TCX files
- Celery worker setup with Redis broker
- Background workers: GPX/FIT/TCX parser, route geometry processor
- Deduplication logic via `external_id`

**Definition of Done:**
- [ ] All new models migrated to database
- [ ] User can connect Strava account via OAuth2
- [ ] New Strava activity triggers webhook → activity saved to DB
- [ ] User can upload a GPX file → activity parsed and saved to DB
- [ ] Duplicate activities are rejected gracefully
- [ ] Celery worker processes files in background without blocking HTTP

**Dependencies:** Phase 1 complete

---

## Phase 3 — API Layer

**Goal:** Expose all stored data via a clean, documented REST API.

**Deliverables:**
- `GET /api/v1/workouts` — list workouts with filtering and pagination
- `GET /api/v1/workouts/{id}` — single workout with full details + route GeoJSON
- `GET /api/v1/metrics` — health metrics with time range filtering
- `GET /api/v1/stats` — aggregated statistics (total distance, elevation, time)
- `GET /api/v1/gear` — gear list with total distance
- `PATCH /api/v1/users/me` — update user preferences
- TimescaleDB hypertables for `workouts` and `metrics`
- PostGIS spatial queries for route data
- Redis caching for expensive aggregation queries

**Definition of Done:**
- [ ] All endpoints return correct data with proper pagination
- [ ] Route data returned as valid GeoJSON
- [ ] Statistics queries use TimescaleDB time-bucket functions
- [ ] Cached responses return within 50ms on repeat calls
- [ ] All endpoints documented in OpenAPI / Swagger UI

**Dependencies:** Phase 2 complete

---

## Phase 4 — UI + Orchestration

**Goal:** Build the frontend dashboard and set up automated sync workflows.

**Deliverables:**
- React + Vite SPA with React Router
- Pages: Dashboard, Activity List, Activity Detail, Settings, Login
- Components: ActivityCard, RouteMap (Leaflet), MetricChart (Recharts), StatWidget
- Strava connect button + OAuth callback flow in UI
- n8n workflow: Strava webhook handler
- n8n workflow: Scheduled Strava sync (fallback polling)
- State management with Zustand or Redux Toolkit
- API client with axios + auth token interceptor

**Definition of Done:**
- [ ] User can log in and see their dashboard
- [ ] Activity list shows all synced workouts with key stats
- [ ] Activity detail shows route on interactive map
- [ ] User can connect Strava from Settings page
- [ ] n8n automatically syncs new Strava activities within 5 minutes
- [ ] App is responsive on mobile

**Dependencies:** Phase 3 complete

---

## Phase 5 — Production

**Goal:** Make the application deployable, observable, and maintainable on a homelab server.

**Deliverables:**
- Production `docker-compose.yml` — all services containerized
- `docker-compose.override.yml` for dev vs prod config separation
- Nginx production config with SSL termination
- GitHub Actions: CI pipeline (lint, test, build)
- GitHub Actions: CD pipeline (deploy on push to main)
- Automated database backup script (`scripts/backup.sh`)
- Restore script (`scripts/restore.sh`)
- `docs/self-hosting.md` — complete step-by-step deployment guide
- Health monitoring — basic uptime checks
- Log aggregation setup

**Definition of Done:**
- [ ] `docker compose up -d` on a fresh server brings up the full stack
- [ ] SSL certificate configured and HTTPS working
- [ ] CI runs on every PR — lint, test, build must pass
- [ ] Automated daily DB backup running
- [ ] self-hosting.md allows a technical user to deploy from scratch in under 30 minutes

**Dependencies:** Phase 4 complete

---

## Branching Strategy per Phase

Each phase gets its own branch off `develop`:

```
main          ← stable, tagged releases only
develop       ← integration branch
phase/2-data-ingestion   ← current
phase/3-api-layer
phase/4-ui-orchestration
phase/5-production
```

Merge to `develop` when phase is complete, then `develop` → `main` for releases.
