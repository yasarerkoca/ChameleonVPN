from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

class GeoIPBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        try:
            # Ülke bazlı filtre vs. (şimdilik pas)
            return await call_next(request)
        except Exception:
            return await call_next(request)

async def geoip_block_middleware(request, call_next):
    return await GeoIPBlockMiddleware(None).dispatch(request, call_next)
