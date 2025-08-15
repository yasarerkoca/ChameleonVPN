# app/middleware/enforce_2fa.py
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.utils.auth.auth_utils import get_current_user

class Enforce2FAMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # /auth/login ve /auth/2fa dışında kontrol uygula
        if request.url.path.startswith("/auth/") and not request.url.path.startswith("/auth/2fa"):
            return await call_next(request)
        user = await get_current_user(request)
        if user and not user.is_2fa_verified:
            return JSONResponse(status_code=403, content={"detail": "2FA zorunlu. Lütfen doğrulama yapınız."})
        return await call_next(request)
