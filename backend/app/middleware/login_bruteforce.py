import json
import time
from typing import Optional

from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from sqlalchemy.exc import SQLAlchemyError
import logging

from .common import should_bypass

logger = logging.getLogger(__name__)

# Opsiyonel DB fonksiyonları (varsa kullanırız)
try:
    from app.config.database import SessionLocal  # type: ignore
except ImportError:  # pragma: no cover
    SessionLocal = None  # type: ignore

try:
    from app.crud.security.failed_login_attempt_crud import (  # type: ignore
        log_failed_attempt,
        count_recent_failed_attempts,
        clear_failed_attempts,
    )
except ImportError:  # pragma: no cover
    log_failed_attempt = count_recent_failed_attempts = clear_failed_attempts = None  # type: ignore

# Yalnızca aşağıdaki login yollarında devreye gir
LOGIN_PATHS = {"/auth/login", "/auth/2fa/login-totp"}

# Limitler (in-memory fallback için, DB katmanı kendi zaman penceresini kullanabilir)
ATTEMPT_LIMIT = 5
WINDOW_SECONDS = 60

# In-memory pencere; DB yoksa bunu kullanırız
_ATTEMPT_CACHE: dict[str, int] = {}


def _client_ip(req: Request) -> str:
    xff = req.headers.get("x-forwarded-for", "")
    if xff:
        return xff.split(",")[0].strip()
    return req.client.host if req.client else "0.0.0.0"


def _memory_guard(ip: str) -> None:
    """Sabit pencere sayaçla IP başına deneme sınırı uygula."""
    bucket = int(time.time()) // WINDOW_SECONDS
    key = f"{ip}:{bucket}"
    cnt = _ATTEMPT_CACHE.get(key, 0)
@@ -63,65 +67,67 @@ class LoginBruteForceMiddleware(BaseHTTPMiddleware):
        # DB katmanı mevcutsa onu kullan
        db_guard_available = all(
            [
                SessionLocal,
                count_recent_failed_attempts,
                log_failed_attempt,
                clear_failed_attempts,
            ]
        )

        try:
            if db_guard_available:
                # DB bağlantısı
                db = SessionLocal()  # type: ignore

                # Son X süre içindeki başarısız denemeleri say
                fails = count_recent_failed_attempts(db, ip)  # type: ignore
                if fails >= ATTEMPT_LIMIT:
                    raise HTTPException(status_code=429, detail="Çok fazla başarısız giriş denemesi")

                # Body'yi bir kez okuyup alttaki handler kullanabilsin
                body = await request.body()
                request._body = body  # starlette: tekrar okunabilsin
                try:
                    email: Optional[str] = json.loads(body.decode() or "{}").get("email")
                except ValueError:
                    email = None

                response = await call_next(request)

                # Başarısızsa logla; başarılıysa temizle
                if response.status_code >= 400:
                    try:
                        log_failed_attempt(db, ip, email)  # type: ignore
                    except SQLAlchemyError as exc:
                        logger.warning("Failed to log failed attempt: %s", exc)
                else:
                    try:
                        clear_failed_attempts(db, ip)  # type: ignore
                    except SQLAlchemyError as exc:
                        logger.warning("Failed to clear failed attempts: %s", exc)

                return response

            # DB yoksa in-memory fallback
            _memory_guard(ip)
            return await call_next(request)

        except HTTPException:
        except SQLAlchemyError as exc:
            logger.error("Login brute force middleware DB error: %s", exc)
            raise HTTPException(status_code=503, detail="Service temporarily unavailable")
        except Exception as exc:
            logger.error("Login brute force middleware error: %s", exc)
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            if db:
                try:
                    db.close()
                except SQLAlchemyError as exc:
                    logger.warning("Failed to close DB session: %s", exc)


# Fonksiyon şeklinde kullanıldıysa uyumluluk için alias
async def login_bruteforce_middleware(request, call_next):
    return await LoginBruteForceMiddleware(None).dispatch(request, call_next)

