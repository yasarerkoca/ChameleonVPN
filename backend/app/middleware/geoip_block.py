"""GeoIP tabanlı ülke engelleme middleware'i."""

import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi.responses import JSONResponse
from .common import should_bypass

# Opsiyonel GeoIP kütüphanesi importu
try:
    from app.utils.geo.geoip_utils import get_country_by_ip  # type: ignore
except Exception:  # pragma: no cover
    get_country_by_ip = None  # type: ignore

class GeoIPBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)

        blocked_countries = {
            c.strip().upper()
            for c in os.getenv("GEOIP_BLOCKED_COUNTRIES", "").split(",")
            if c.strip()
        }
        # Liste boşsa veya GeoIP kullanılamıyorsa akışı bozma
        if not blocked_countries or not get_country_by_ip:
            return await call_next(request)

        xff = request.headers.get("x-forwarded-for", "")
        client_ip = (xff.split(",")[0].strip() if xff else None) or (
            request.client.host if request.client else "0.0.0.0"
        )

        try:
            country = get_country_by_ip(client_ip)
            if country in blocked_countries:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "Erişiminiz bulunduğunuz ülke nedeniyle engellendi."},
                )
        except Exception:
            pass

        return await call_next(request)

async def geoip_block_middleware(request, call_next):
    return await GeoIPBlockMiddleware(None).dispatch(request, call_next)
