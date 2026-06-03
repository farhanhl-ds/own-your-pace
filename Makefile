.PHONY: dev dev-setup test lint migrate logs down requirements

dev:
	docker compose up -d db redis n8n
	cd backend && uvicorn app.main:app --reload &
	cd frontend && npm run dev

dev-setup:
	cp .env.example .env
	cd backend && python -m venv .venv && .venv/bin/pip install -e ".[dev]"
	cd frontend && npm install

migrate:
	docker compose exec api alembic upgrade head

test:
	cd backend && pytest --cov=app
	cd frontend && npm run test

lint:
	cd backend && ruff check . && ruff format --check .
	cd frontend && npm run lint

logs:
	docker compose logs -f api worker

down:
	docker compose down

requirements:
	cd backend && pip-compile pyproject.toml --strip-extras --output-file requirements.txt
