SKIP_PATHS={"/docs","/openapi.json","/redoc","/metrics"}
# ~/ChameleonVPN/backend/app/middleware/mfa_required.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from app.utils.auth.auth_utils import get_current_user_optional

BYPASS_PATHS = [
    "/auth/login",
    "/auth/register",
    "/auth/2fa/verify",
    "/auth/password/forgot",
    "/auth/password/reset",
    "/docs", "/openapi.json", "/redoc"
]

class MFARequiredMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Sadece /auth/login dışındaki her endpointte kontrol
        if any(request.url.path.startswith(path) for path in BYPASS_PATHS):
            
    if request.url.path in SKIP_PATHS:
        return await call_next(request)
    return await call_next(request)

        try:
            user = await get_current_user_optional(request)
            if user and not user.is_2fa_verified:
                return JSONResponse(status_code=403, content={"detail": "2FA doğrulanmalı!"})
        except Exception:
            pass  # Girişsiz istekler (ör: public health endpoint) için geç
        return await call_next(request)
