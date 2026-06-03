# Architecture Overview

> own-your-pace — Self-hosted fitness data aggregator. Sync once, own forever.

---

## System Overview

own-your-pace is a self-hosted backend system that pulls fitness activity data
from external providers (Strava) and stores it permanently in a PostgreSQL database
on your own server. It is not a social platform or a Strava replacement — it is a
personal data ownership layer.

```
External Providers          Orchestration        Backend            Storage
─────────────────           ─────────────        ───────            ───────
Strava (webhook)   ──────►  n8n workflows  ────► FastAPI  ────────► PostgreSQL
Strava (polling)   ──────►                       REST API           TimescaleDB
Manual GPX/FIT     ──────────────────────────►              ──────► PostGIS
                                                      │
                                                      ▼
                                                    Redis
                                               (cache + queue)
                                                      │
                                                      ▼
                                               Celery Workers
                                           (file processing, sync)
```

---

## Component Breakdown

### FastAPI (Backend)
The core of the system. Owns all business logic, data validation, authentication,
and database writes. n8n never writes to the database directly — it always goes
through FastAPI endpoints.

Runs locally during development (`uvicorn --reload`), containerized in production.

### PostgreSQL + TimescaleDB + PostGIS
Single database instance with three extensions:
- **TimescaleDB** — optimizes time-series queries on `workouts` and `metrics` tables
- **PostGIS** — enables spatial storage and queries for GPS routes (`geometry` type)
- **uuid-ossp** — server-side UUID generation

### Redis
Dual-purpose:
- **Cache** — API response caching for expensive queries (statistics, aggregations)
- **Celery broker** — task queue for background jobs (GPX processing, batch sync)

### Celery Workers
Background job processors. Handles tasks that shouldn't block HTTP requests:
- Parsing and processing uploaded GPX/FIT/TCX files
- Batch activity sync
- Notifications

### n8n
External sync orchestrator. Handles:
- OAuth2 token storage and automatic refresh for Strava
- Scheduled polling (Google Fit, fallback sync)
- Strava webhook event forwarding
- Transform raw provider payload → FastAPI-compatible format
- Retry logic on failed requests

n8n communicates with FastAPI via HTTP using an internal API key.
All business logic (dedup, validation, normalization) stays in FastAPI.

### React + Vite (Frontend)
Single-page application. Consumes FastAPI REST endpoints.
Key views: dashboard, activity list, activity detail with GPS map, stats/charts.

### Nginx
Reverse proxy and single entry point. Routes:
- `/api/*` → FastAPI (port 8000)
- `/*` → React frontend (port 5173 dev / static files prod)

---

## Async Task Boundaries

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

---

## Data Flow

### Strava Activity Sync (Webhook — primary)
```
1. User completes activity on Strava
2. Strava sends POST to n8n webhook endpoint
3. n8n transforms payload and forwards to POST /api/v1/sync/strava/activity
4. FastAPI validates, checks for duplicate (external_id), saves to DB
5. Celery worker processes GPS data (route geometry, lap splits) async
```

### Manual File Upload
```
1. User uploads GPX/FIT/TCX via frontend
2. FastAPI saves file to /uploads, returns 202 Accepted
3. Celery worker picks up job, parses file, extracts:
   - Activity metadata (duration, distance, elevation)
   - GPS track → PostGIS LineString geometry
   - Lap data → laps table
4. Worker saves parsed data to workouts table
```

---

## Database Schema Summary

| Table | Type | Notes |
|---|---|---|
| `users` | Standard | Auth, preferences |
| `workouts` | TimescaleDB hypertable | Core activity data, PostGIS route |
| `laps` | Standard | Per-lap splits, FK to workouts |
| `metrics` | TimescaleDB hypertable | Steps, HR, sleep — high frequency |
| `sync_sources` | Standard | OAuth tokens per provider per user |
| `sports` | Standard | Lookup table (run, ride, swim, etc.) |
| `gear` | Standard | Shoes, bikes — with distance tracking |
| `workout_gear` | Junction | Many-to-many workouts ↔ gear |

---

## Architecture Decision Records (ADR)

### ADR-001: PostgreSQL over InfluxDB for time-series
**Decision:** Use PostgreSQL + TimescaleDB instead of a dedicated time-series DB.
**Reason:** Fitness data has strong relational structure (user → workout → laps → gear).
Pure time-series DBs lack JOIN capability and make relational queries awkward.
TimescaleDB gives time-series performance while keeping full SQL expressiveness.

### ADR-002: n8n as external agent, not embedded scheduler
**Decision:** n8n runs as a separate service, communicates via HTTP.
**Reason:** Keeps all business logic in one place (FastAPI). If n8n is replaced
with Prefect or APScheduler later, zero application code changes needed.

### ADR-003: Separate models/ and schemas/
**Decision:** SQLAlchemy ORM models and Pydantic schemas are always in separate files.
**Reason:** ORM models represent DB structure; schemas represent API contracts.
Mixing them causes tight coupling and makes both harder to evolve independently.

### ADR-004: PostGIS geometry over JSON for GPS tracks
**Decision:** Store GPS routes as `geometry(LineString, 4326)` via GeoAlchemy2.
**Reason:** Enables spatial indexing, distance queries, bounding box filters,
and GeoJSON serialization. JSON arrays have none of these capabilities.

### ADR-005: Celery over APScheduler for background jobs
**Decision:** Use Celery with Redis broker for background processing.
**Reason:** Celery supports named queues (gpx, sync, default), retry policies,
task monitoring, and horizontal scaling. APScheduler is in-process only.

### ADR-006: n8n owns external, Celery owns internal async
**Decision:** Strict boundary between n8n and Celery responsibilities.
**Reason:** n8n is optimized for orchestrating external API interactions —
OAuth flows, retries, webhooks, and multi-step provider pipelines. Celery is
optimized for heavy internal computation that shouldn't block HTTP requests.
Mixing these concerns in either tool makes both harder to debug and maintain.

### ADR-007: Huawei Health via Strava bridge
**Decision:** No direct Huawei Health API integration.
**Reason:** Huawei Health Kit is HMS mobile SDK only — not designed for
server-to-server. Auto-sync Huawei Health → Strava handles this transparently.

### ADR-008: Google Fit dropped from v1 scope
**Decision:** Google Fit REST API not integrated.
**Reason:** Google Fit API is deprecated as of 2024 and shutting down in 2026.
New developer registrations closed May 2024. Not worth building against.