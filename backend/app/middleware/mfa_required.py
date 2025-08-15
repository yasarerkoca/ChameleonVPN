from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

class MFARequiredMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        try:
            # MFA gerekli alanlar (şimdilik pas)
            return await call_next(request)
        except Exception:
            return await call_next(request)
