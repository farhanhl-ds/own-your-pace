from collections.abc import Generator
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,       # auto-reconnect if connection lost
    pool_size=10,
    max_overflow=20,
    echo=settings.debug,      # log SQL queries if debug=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency — inject DB session ke route handler."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
