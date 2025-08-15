# ~/ChameleonVPN/backend/app/middleware/login_bruteforce.py

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.db.db_utils import get_db
from app.crud.security.failed_login_attempt_crud import (
    log_failed_attempt, count_recent_failed_attempts, clear_failed_attempts, clear_old_attempts
)
from app.crud.security.blocked_ip_crud import block_ip, is_ip_blocked

MAX_FAIL = 5
BAN_MINUTES = 15

class LoginBruteForceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path == "/auth/login":
            ip = request.client.host
            db = next(get_db())
            # IP blokluysa direkt 429 dön
            if is_ip_blocked(db, ip):
                return JSONResponse(
                    status_code=429,
                    content={"detail": "Çok fazla başarısız giriş! IP banlandı."}
                )
            response = await call_next(request)
            if response.status_code == 401:
                try:
                    payload = await request.json()
                    username = payload.get("username") or payload.get("email")
                except Exception:
                    username = None
                log_failed_attempt(db, ip, username)
                if count_recent_failed_attempts(db, ip, window_minutes=BAN_MINUTES) >= MAX_FAIL:
                    block_ip(db, ip, reason="Brute-force detect", minutes=BAN_MINUTES)
                    return JSONResponse(
                        status_code=429,
                        content={"detail": f"IP adresiniz {BAN_MINUTES} dakika banlandı."}
                    )
                clear_failed_attempts(db, ip)
            return response
        return await call_next(request)
