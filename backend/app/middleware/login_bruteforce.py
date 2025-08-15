from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Dokümantasyon/health gibi uçlar DB/Redis'e dokunmasın
SKIP_PATHS = {"/docs", "/openapi.json", "/redoc", "/metrics", "/healthz"}

class LoginBruteForceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path
        if path in SKIP_PATHS or path.startswith("/static"):
            return await call_next(request)

        # TODO: Brute-force kontrolü (Redis/DB) burada uygulanacak
        return await call_next(request)
