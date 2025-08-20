import asyncio
import os

from cachetools import TTLCache
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from .common import should_bypass

SESSION_CACHE_TTL = int(os.getenv("SESSION_CACHE_TTL", "3600"))
SESSION_CACHE_MAXSIZE = int(os.getenv("SESSION_CACHE_MAXSIZE", "10000"))

SESSION_CACHE = TTLCache(maxsize=SESSION_CACHE_MAXSIZE, ttl=SESSION_CACHE_TTL)
SESSION_LOCK = asyncio.Lock()

class SessionHijackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Statik yolları bypass et
        if should_bypass(request):
            return await call_next(request)

        try:
            session_id = request.cookies.get("session_id") or request.headers.get("authorization")
            if session_id:
                ip = request.client.host if request.client else "0.0.0.0"
                ua = request.headers.get("user-agent", "")

                async with SESSION_LOCK:
                    known = SESSION_CACHE.get(session_id)
                    if known is None:
                        SESSION_CACHE[session_id] = (ip, ua)
                    elif known != (ip, ua):
                        raise HTTPException(status_code=403, detail="Session hijack detected")


            return await call_next(request)
        except HTTPException:
            raise
        except Exception:
            return await call_next(request)
