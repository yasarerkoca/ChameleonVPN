from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

# Opsiyonel DB erişimi (varsa) – yoksa no-op
try:
    from app.crud.security.blocked_ip_crud import is_ip_blocked  # type: ignore
    from app.db.session import SessionLocal  # type: ignore
except Exception:
    is_ip_blocked = None
    SessionLocal = None

class IPBlockMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        # DB yoksa veya hata olursa kesinlikle akışı kesme
        if is_ip_blocked and SessionLocal:
            try:
                db = SessionLocal()
                client_ip = request.client.host if request.client else "0.0.0.0"
                try:
                    if is_ip_blocked(db, client_ip):  # türüne göre True/False bekler
                        # Bloğu uygulamak istersen burada Response dönebilirsin.
                        # Şimdilik production'ı kırmamak için devam:
                        pass
                finally:
                    db.close()
            except Exception:
                pass
        return await call_next(request)

async def ip_block_middleware(request, call_next):
    return await IPBlockMiddleware(None).dispatch(request, call_next)
