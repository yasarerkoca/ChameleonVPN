# ~/ChameleonVPN/backend/app/services/jwt_service.py

"""Utility functions for creating and verifying JWT tokens.

Centralizes creation and validation of all token types used in the
application: access, refresh, email verification and password reset.

All expiration times and algorithms are configured via the application
settings to avoid hard-coded values in the codebase.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from jose import jwt, JWTError

from app.config.base import settings


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create a signed refresh token."""
    expire = datetime.utcnow() + (
        expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_password_reset_token(
    email: str, expires_delta: Optional[timedelta] = None
) -> str:

    """Create a password reset token for the given e-mail address."""
    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(minutes=settings.PASSWORD_RESET_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify a password reset token and return the e-mail address if valid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None
def create_email_verification_token(
    email: str, expires_delta: Optional[timedelta] = None
) -> str:
    """Create an e-mail verification token for the given e-mail address."""
    expire = datetime.utcnow() + (
        expires_delta
        or timedelta(minutes=settings.EMAIL_VERIFICATION_TOKEN_EXPIRE_MINUTES)
    )
    to_encode = {"sub": email, "exp": expire}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_email_verification_token(token: str) -> Optional[str]:
    """Verify an e-mail verification token and return the address if valid."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


def decode_token(token: str) -> Optional[Dict]:
    """Decode a JWT and return its payload or ``None`` if invalid."""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None
# Backwards compatibility alias
decode_access_token = decode_token


__all__ = [
    "create_access_token",
    "create_refresh_token",
    "create_password_reset_token",
    "verify_password_reset_token",
    "create_email_verification_token",
    "verify_email_verification_token",
    "decode_token",
    "decode_access_token",
]

