from datetime import datetime, timezone

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.security import decode_token, TokenBlocklist
from app.core.config import get_settings
from app.models.user import User

settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Decode JWT, verify token type, check blocklist, and return the active user.

    Raises HTTP 401 if the token is invalid, expired, revoked, or belongs to an
    inactive account. This is the single source of truth for authentication
    — do not add a second is_active check downstream.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        jti: str | None = payload.get("jti")

        if user_id is None or payload.get("type") != "access":
            raise credentials_exception

        # Reject revoked tokens (e.g. after logout)
        if jti and TokenBlocklist.is_revoked(jti):
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


# Alias — kept for route handler readability.
# Both resolve to the same dependency; is_active is already checked above.
get_current_active_user = get_current_user
