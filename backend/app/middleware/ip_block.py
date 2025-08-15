# ~/ChameleonVPN/backend/app/middleware/ip_block.py
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

# Opsiyonel DB erişimi (varsa) – yoksa no-op
try:
    from app.crud.security.blocked_ip_crud import is_ip_blocked  # type: ignore
except Exception:
    is_ip_blocked = None  # type: ignore

# SessionLocal: modern yol + legacy fallback
try:
    from app.config.database import SessionLocal  # type: ignore
except Exception:  # pragma: no cover
    try:
        from app.config.database import SessionLocal  # type: ignore
    except Exception:
        SessionLocal = None  # type: ignore


class IPBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Sağlık/OpenAPI vb. bypass
        if should_bypass(request):
            return await call_next(request)

        # DB ve fonksiyon mevcutsa kontrol et; hata olursa sessiz geç
        if is_ip_blocked and SessionLocal:
            db = None
            try:
                db = SessionLocal()

                # Proxy arkasında isek ilk XFF IP; yoksa client.host
                xff = request.headers.get("x-forwarded-for", "")
                client_ip = (xff.split(",")[0].strip() if xff else None) or (
                    request.client.host if request.client else "0.0.0.0"
                )

                try:
                    if is_ip_blocked(db, client_ip):
                        # Şimdilik prod’u kırmamak için sadece akışı sürdür.
                        # İstersen burada 403 dönecek şekilde değiştirebiliriz.
                        pass
                finally:
                    db.close()
            except Exception:
                if db:
                    try:
                        db.close()
                    except Exception:
                        pass

        return await call_next(request)


async def ip_block_middleware(request, call_next):
    return await IPBlockMiddleware(None).dispatch(request, call_next)
