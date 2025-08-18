from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

# Basit bellek içi oturum takibi
_SESSION_CACHE = {}


class SessionHijackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Statik yolları bypass et
        if should_bypass(request):
            return await call_next(request)
        auth_header = request.headers.get("authorization")
        if not auth_header:
            return await call_next(request)

        token = auth_header.split(" ")[-1]

        xff = request.headers.get("x-forwarded-for", "")
        client_ip = (xff.split(",")[0].strip() if xff else None) or (
            request.client.host if request.client else "0.0.0.0"
        )
        ua = request.headers.get("user-agent", "")

        session = _SESSION_CACHE.get(token)
        if session:
            if session["ip"] != client_ip or session["ua"] != ua:
                raise HTTPException(status_code=403, detail="Olası oturum ele geçirme tespit edildi")
        else:
            _SESSION_CACHE[token] = {"ip": client_ip, "ua": ua}

        return await call_next(request)
