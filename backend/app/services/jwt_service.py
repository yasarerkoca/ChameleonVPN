"""Centralizes creation and validation of all token types used in the
application: access, refresh, email verification and password reset.

All expiration times and algorithms are configured via the application
settings to avoid hard-coded values in the codebase.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
from fastapi import HTTPException
from jose import jwt, JWTError

from app.config.base import settings
from . import token_blacklist


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


def revoke_refresh_token(token: str) -> None:
    """Blacklist the provided refresh token using Redis."""
    payload = decode_token(token)
    if not payload:
        return
    exp = datetime.utcfromtimestamp(payload.get("exp", 0))
    token_blacklist.add(token, exp)


def refresh_tokens(refresh_token: str) -> Dict[str, str]:
    """Rotate refresh tokens and issue a new token pair.

    Raises ``HTTPException`` if the provided refresh token is invalid or
    has been revoked.
    """
    if token_blacklist.contains(refresh_token):
        raise HTTPException(status_code=401, detail="Refresh token revoked")

    payload = decode_token(refresh_token)
    if payload is None:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Revoke old token and issue new pair
    revoke_refresh_token(refresh_token)

    data = {"sub": payload.get("sub"), "user_id": payload.get("user_id")}
    access = create_access_token(data)
    refresh = create_refresh_token(data)
    return {"access_token": access, "refresh_token": refresh, "token_type": "bearer"}


# --- Backwards compatibility aliases ---
decode_access_token = decode_token

def encode(payload: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Alias for create_access_token (for backward compatibility)."""
    return create_access_token(payload, expires_delta)

def decode(token: str) -> Optional[Dict]:
    """Alias for decode_token (for backward compatibility)."""
    return decode_token(token)


__all__ = [
    "create_access_token",
    "create_refresh_token",
    "create_password_reset_token",
    "verify_password_reset_token",
    "create_email_verification_token",
    "verify_email_verification_token",
    "decode_token",
    "decode_access_token",
    "refresh_tokens",
    "revoke_refresh_token",
    "encode",
    "decode",
]
