# ~/ChameleonVPN/backend/app/middleware/mfa_enforcement.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.auth.auth_utils import get_current_user_jwt

# Sadece /auth ve /docs ve kök (/) dışında kalan her istek için kontrol uygula
EXEMPT_PATHS = [
    "/auth/login", "/auth/register", "/auth/2fa/verify", "/auth/2fa/login-totp",
    "/auth/2fa/generate-totp-secret", "/auth/2fa/send-code",
    "/auth/password/forgot", "/auth/password/reset",
    "/docs", "/openapi.json", "/", "/redoc"
]

class MFAEnforcementMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Sadece JWT ile login gerektiren endpointlerde çalışsın
        if any(request.url.path.startswith(p) for p in EXEMPT_PATHS):
            return await call_next(request)
        try:
            user = await get_current_user_jwt(request)
            # User login ise ve 2FA doğrulaması yoksa erişimi engelle
            if user and not getattr(user, "is_2fa_verified", False):
                return JSONResponse(
                    status_code=403,
                    content={"detail": "2FA doğrulaması zorunlu! Lütfen kodu giriniz."}
                )
        except Exception:
            pass  # Auth olmayanlar için de (ör: public endpoint) normal devam et
        return await call_next(request)
