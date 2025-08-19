"""Redis-backed service for storing revoked refresh tokens.

Tokens are kept with an expiry so Redis automatically clears out
old entries once the original token would have expired."""

from __future__ import annotations

from datetime import datetime
import hashlib
from typing import Optional

import redis

from app.config.base import settings

# Create a synchronous Redis client. The ``redis`` package already exists in the
# project as it is used for rate limiting, so we reuse it here.  Using a
# synchronous client keeps the service simple and allows usage from both
# synchronous and asynchronous contexts without ``await``.
_client: redis.Redis = redis.Redis.from_url(
    settings.REDIS_URL, decode_responses=True
)

_PREFIX = "refresh_blacklist:"


def _key(token: str) -> str:
    """Return a hashed redis key for the given token."""
    digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
    return f"{_PREFIX}{digest}"


def add(token: str, expires_at: datetime) -> None:
    """Store ``token`` in Redis until ``expires_at``.

    Args:
        token: The refresh token to blacklist.
        expires_at: Expiration time of the token. Redis TTL will be derived
            from this value. If the token is already expired, nothing is stored.
    """

    ttl = int((expires_at - datetime.utcnow()).total_seconds())
    if ttl > 0:
        _client.setex(_key(token), ttl, "1")


def contains(token: str) -> bool:
    """Return ``True`` if ``token`` has been revoked."""

    return bool(_client.exists(_key(token)))


__all__ = ["add", "contains"]
