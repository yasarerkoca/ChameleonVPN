import json
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

# Opsiyonel DB fonksiyonları
try:
    from app.crud.security.failed_login_attempt_crud import (
        log_failed_attempt,
        count_recent_failed_attempts,
        clear_failed_attempts,
    )  # type: ignore
except Exception:  # pragma: no cover
    log_failed_attempt = count_recent_failed_attempts = clear_failed_attempts = None  # type: ignore

try:
    from app.config.database import SessionLocal  # type: ignore
except Exception:  # pragma: no cover
    try:
        from app.config.database import SessionLocal  # type: ignore
    except Exception:
        SessionLocal = None  # type: ignore

LOGIN_PATHS = {"/auth/login", "/auth/2fa/login-totp"}
MAX_ATTEMPTS = 5

class LoginBruteForceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        # Bypass yollar veya login dışı istekler
        if should_bypass(request) or request.url.path not in LOGIN_PATHS:
            return await call_next(request)

        # Gerekli DB fonksiyonları yoksa işlemi atla
        if not (SessionLocal and count_recent_failed_attempts and log_failed_attempt and clear_failed_attempts):
            return await call_next(request)
        # IP tespiti
        xff = request.headers.get("x-forwarded-for", "")
        client_ip = (xff.split(",")[0].strip() if xff else None) or (
            request.client.host if request.client else "0.0.0.0"
        )

        db = None
        email = None
        try:
            db = SessionLocal()
            # Son X dakikadaki başarısız giriş sayısını kontrol et
            fails = count_recent_failed_attempts(db, client_ip)
            if fails >= MAX_ATTEMPTS:
                raise HTTPException(status_code=429, detail="Çok fazla başarısız giriş denemesi")

            # Body'yi oku (alttaki endpoint tekrar kullanabilsin)
            body = await request.body()
            request._body = body
            try:
                email = json.loads(body.decode() or "{}").get("email")
            except Exception:
                email = None

            response = await call_next(request)

            # Başarısızlık durumunu logla / başarıda temizle
            if response.status_code >= 400:
                try:
                    log_failed_attempt(db, client_ip, email)
                except Exception:
                    pass
            else:
                try:
                    clear_failed_attempts(db, client_ip)
                except Exception:
                    pass

            return response
        except HTTPException:
            raise
        except Exception:
            # Middleware'de hata olursa sessizce devam et
            return await call_next(request)
        finally:
            if db:
                try:
                    db.close()
                except Exception:
                    pass
# Fonksiyon şeklinde kullanıldıysa uyumluluk için alias
async def login_bruteforce_middleware(request, call_next):
    return await LoginBruteForceMiddleware(None).dispatch(request, call_next)
