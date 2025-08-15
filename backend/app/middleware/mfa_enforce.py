from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.auth.auth_utils import get_current_user

EXEMPT_PATHS = [
    "/auth/login",
    "/auth/register",
    "/auth/2fa/verify",
    "/auth/2fa/generate-totp-secret",
    "/auth/2fa/login-totp",
    "/docs", "/openapi.json", "/redoc"
]

class MFAEnforceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Sadece API endpointlerinde kontrol et, exempt edilenler hariç
        if any(request.url.path.startswith(p) for p in EXEMPT_PATHS):
            return await call_next(request)
        try:
            user = await get_current_user(request)
            if user and not user.is_2fa_verified:
                return JSONResponse(
                    status_code=403,
                    content={"detail": "2FA zorunlu. Lütfen 2FA doğrulaması yapın."}
                )
        except Exception:
            pass
        return await call_next(request)
