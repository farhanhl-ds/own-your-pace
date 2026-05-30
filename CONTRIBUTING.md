# Contributing to FitClone

Thanks for taking the time to contribute! This guide will get you up and running.

---

## Dev environment setup

**Prerequisites:** Python 3.12+, Node.js 20+, Docker, Docker Compose.

```bash
# Clone and enter repo
git clone https://github.com/yourusername/fitclone.git
cd fitclone

# Copy env
cp .env.example .env

# Start dependencies only (DB + Redis + n8n)
docker compose up -d db redis n8n

# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install
npm run dev
```

---

## Branch strategy

| Branch | Purpose |
|---|---|
| `main` | Stable, always deployable |
| `develop` | Integration branch |
| `feature/xxx` | New features |
| `fix/xxx` | Bug fixes |
| `docs/xxx` | Documentation only |

Always branch off `develop`, never directly off `main`.

---

## Commit messages

Follow [Conventional Commits](https://www.conventionalcommits.org):

```
feat: add Strava webhook endpoint
fix: handle duplicate activity on sync
docs: update self-hosting guide
chore: bump FastAPI to 0.111
refactor: extract GPX parser to service layer
test: add unit tests for sync deduplication
```

---

## Running tests

```bash
# Backend
cd backend
pytest                        # all tests
pytest -k "test_workout"      # filter by name
pytest --cov=app              # with coverage

# Frontend
cd frontend
npm run test
npm run type-check
```

---

## Code style

**Python:** `ruff` for linting and formatting. Config in `pyproject.toml`.
```bash
ruff check .
ruff format .
```

**TypeScript/React:** ESLint + Prettier. Config in `frontend/.eslintrc`.
```bash
npm run lint
npm run format
```

---

## Submitting a PR

1. Fork the repo and create a branch from `develop`
2. Make your changes and add tests where applicable
3. Ensure all tests pass and linting is clean
4. Open a PR against `develop` — not `main`
5. Fill in the PR template

For large changes, please open an issue first to discuss the approach.

---

## Reporting bugs

Use the GitHub issue template. Include:
- Steps to reproduce
- Expected vs actual behavior
- Logs if relevant (`docker compose logs api`)
- Your OS and Docker version
