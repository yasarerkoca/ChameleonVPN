from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

class LoginBruteForceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        try:
            # Sadece giriş endpoint'lerinde (örnek) kontrol yapılabilir.
            # Şimdilik geçiş:
            return await call_next(request)
        except Exception:
            # Middleware iç hatasında akışı kesme
            return await call_next(request)

# Fonksiyon şeklinde kullanıldıysa uyumluluk için alias
async def login_bruteforce_middleware(request, call_next):
    return await LoginBruteForceMiddleware(None).dispatch(request, call_next)
