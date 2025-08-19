from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from .common import should_bypass
from app.utils.auth.auth_utils import get_current_user_jwt

EXEMPT_PATHS = [
    "/auth/login",
    "/auth/register",
    "/auth/2fa/verify",
    "/auth/2fa/generate-totp-secret",
    "/auth/2fa/login-totp",
    "/auth/2fa/setup",
    "/docs", "/openapi.json", "/redoc"
]

class MFAEnforceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Belirli yolları veya statik içerikleri atla
        if should_bypass(request) or any(request.url.path.startswith(p) for p in EXEMPT_PATHS):
            return await call_next(request)
        try:
            user = await get_current_user_jwt(request)
        except HTTPException:
            return await call_next(request)
        remember_cookie = request.cookies.get("remember_device")
        if user and not getattr(user, "is_2fa_verified", False) and not remember_cookie:
            return JSONResponse(
                status_code=403,
                content={"detail": "2FA zorunlu. Lütfen 2FA doğrulaması yapın."}
            )
        return await call_next(request)
