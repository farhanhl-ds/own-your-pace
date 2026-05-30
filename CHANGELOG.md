# Changelog

All notable changes to this project will be documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
This project uses [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

### Added
- Initial project architecture and database schema
- Docker Compose setup with TimescaleDB + PostGIS + Redis + n8n
- FastAPI project structure with SQLAlchemy + Alembic
- React + Vite frontend scaffold

---

## [0.1.0] - TBD

### Added
- FastAPI backend with JWT authentication
- PostgreSQL schema: users, workouts, metrics, gear, sync_sources
- Strava OAuth2 flow and webhook integration
- GPX/FIT/TCX file upload and parsing
- Celery background workers for file processing
- React dashboard with activity list and basic stats
- n8n workflow for Strava sync
- Nginx reverse proxy configuration
- Comprehensive Docker Compose setup
