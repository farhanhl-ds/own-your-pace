from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,       # auto-reconnect kalau koneksi putus
    pool_size=10,
    max_overflow=20,
    echo=settings.debug,      # log SQL queries kalau debug=True
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Session:
    """FastAPI dependency — inject DB session ke route handler."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
