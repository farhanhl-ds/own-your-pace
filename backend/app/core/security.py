import uuid
from datetime import datetime, timedelta, timezone
from typing import Any

import redis as redis_lib
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ─── Password helpers ─────────────────────────────────────────────────────────

def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


# ─── Token creation ───────────────────────────────────────────────────────────

def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    expire = datetime.now(timezone.utc) + (
        expires_delta or timedelta(minutes=settings.access_token_expire_minutes)
    )
    payload = {
        "sub": str(subject),
        "exp": expire,
        "type": "access",
        "jti": str(uuid.uuid4()),  # unique token ID — used for revocation
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def create_refresh_token(subject: str | Any) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    payload = {
        "sub": str(subject),
        "exp": expire,
        "type": "refresh",
        "jti": str(uuid.uuid4()),  # unique token ID — used for revocation
    }
    return jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)


def decode_token(token: str) -> dict:
    """Decode and validate a JWT. Raises JWTError if the token is invalid or expired."""
    return jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])


# ─── Token blocklist (Redis-backed) ──────────────────────────────────────────

class TokenBlocklist:
    """Redis-backed JWT blocklist for logout / token revocation.

    Stores the jti (JWT ID) of revoked tokens with a TTL matching the
    token's remaining lifetime. Revoked tokens are rejected in get_current_user.
    """

    _client: redis_lib.Redis | None = None

    @classmethod
    def _get_client(cls) -> redis_lib.Redis:
        if cls._client is None:
            cls._client = redis_lib.from_url(
                settings.redis_url,
                decode_responses=True,
            )
        return cls._client

    @classmethod
    def revoke(cls, jti: str, expires_at: datetime) -> None:
        """Add a jti to the blocklist. TTL = remaining token lifetime + 60s buffer."""
        ttl = int((expires_at - datetime.now(timezone.utc)).total_seconds()) + 60
        if ttl > 0:
            cls._get_client().setex(f"blocklist:{jti}", ttl, "1")

    @classmethod
    def is_revoked(cls, jti: str) -> bool:
        """Return True if the jti has been revoked."""
        return cls._get_client().exists(f"blocklist:{jti}") == 1
