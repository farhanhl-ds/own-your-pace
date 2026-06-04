# 🏃 own-your-pace

> Self-hosted fitness data aggregator. Sync once, own forever.

![Build Status](https://img.shields.io/github/actions/workflow/status/farhanhl-ds/own-your-pace/ci.yml?branch=main&style=flat-square)
![License](https://img.shields.io/github/license/farhanhl-ds/own-your-pace?style=flat-square)
![Version](https://img.shields.io/github/v/tag/farhanhl-ds/own-your-pace?style=flat-square)
![Python](https://img.shields.io/badge/python-3.12-blue?style=flat-square)
![Docker](https://img.shields.io/badge/docker-compose-2496ED?style=flat-square&logo=docker&logoColor=white)

---

## ✨ Features

- **Strava sync** — automatic activity sync via webhook, no manual import needed
- **GPS route visualization** — interactive maps powered by OpenStreetMap + PostGIS
- **Health metrics** — track steps, heart rate, sleep, and more over time
- **Manual upload** — import GPX, FIT, and TCX files from any device
- **Self-hosted** — your data stays on your server, always
- **REST API** — full API access with OpenAPI docs included
- **n8n automation** — visual workflow editor for sync orchestration

---

## 🖥️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 18 + TimescaleDB + PostGIS |
| Cache / Queue | Redis 7 + Celery |
| Sync | n8n |
| Frontend | React 18 + Vite |
| Reverse proxy | Nginx |
| Container | Docker + Docker Compose |

---

## 🚀 Quick Start

> Prerequisites: Docker, Docker Compose, and a Strava API app (free).

**1. Clone the repo**
```bash
git clone https://github.com/farhanhl-ds/own-your-pace.git
cd own-your-pace
```

**2. Copy and fill in environment variables**
```bash
cp .env.example .env
# Edit .env — set your Strava credentials, DB password, and SECRET_KEY
```

**3. Start all services**
```bash
docker compose up -d
```

**4. Run database migrations**
```bash
docker compose exec api alembic upgrade head
```

**5. Open the app**

| Service | URL |
|---|---|
| Frontend | http://localhost |
| API docs | http://localhost/api/docs |
| n8n | http://localhost:5678 |

---

## 📂 Project Structure

```
own-your-pace/
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── api/v1/   # Route handlers — auth, workouts, metrics, gear, sync
│   │   ├── core/     # Config, security, dependencies
│   │   ├── models/   # SQLAlchemy ORM models
│   │   ├── schemas/  # Pydantic request/response contracts
│   │   ├── services/ # Business logic
│   │   └── workers/  # Celery background jobs
│   └── db/           # Session, base, Alembic migrations
├── frontend/         # React + Vite SPA
├── n8n/              # Workflow definitions (JSON)
├── nginx/            # Reverse proxy config
├── docs/             # Project documentation
└── scripts/          # Setup, backup, restore
```

---

## 📡 Connecting Strava

1. Go to [strava.com/settings/api](https://www.strava.com/settings/api) and create an app
2. Set **Authorization Callback Domain** to your server's domain (or `localhost`)
3. Copy **Client ID** and **Client Secret** to your `.env`
4. Open the app → **Settings → Integrations → Connect Strava**
5. Authorize — your activities will sync automatically via webhook

---

## 📖 Documentation

- [Architecture overview](docs/architecture.md)
- [Development phases](docs/development-phases.md)
- [Self-hosting guide](docs/self-hosting.md)
- [API reference](docs/api-reference.md)
- [Contributing guide](docs/contributing.md)
- [Changelog](CHANGELOG.md)

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](docs/contributing.md) first.

```bash
make dev-setup   # install dependencies
make dev         # start local dev environment
make test        # run tests
make lint        # lint and format check
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org):
`feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`

---

## 🗺️ Roadmap

See [docs/development-phases.md](docs/development-phases.md) for full details on each phase.

- [x] Phase 1 — Foundation (auth, DB, core setup)
- [ ] Phase 2 — Data Ingestion (Strava webhook, file upload, Celery)
- [ ] Phase 3 — API Layer (workouts, metrics, gear endpoints)
- [ ] Phase 4 — UI + Orchestration (React dashboard, n8n workflows)
- [ ] Phase 5 — Production (CI/CD, monitoring, backup)

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<p align="center">Built with ☕ and too many kilometers logged</p>