import time
import re
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from .common import should_bypass

# Basit bellek içi trafik ve davranış kaydı
_REQUEST_LOG = {}

# Şüpheli UA ve payload desenleri
_BAD_UA = ("curl", "bot", "crawler", "scan")
_SUSPICIOUS_RE = re.compile(r"(union select|drop table|or 1=1|<script)", re.IGNORECASE)
_MAX_PER_MINUTE = 100

class AnomalyFraudDetectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        try:
            # IP ve UA bilgilerini al
            xff = request.headers.get("x-forwarded-for", "")
            client_ip = (xff.split(",")[0].strip() if xff else None) or (
                request.client.host if request.client else "0.0.0.0"
            )
            ua = request.headers.get("user-agent", "").lower()

            # Basit rate limit kontrolü
            now = time.time()
            times = _REQUEST_LOG.setdefault(client_ip, [])
            while times and now - times[0] > 60:
                times.pop(0)
            if len(times) >= _MAX_PER_MINUTE:
                raise HTTPException(status_code=429, detail="Şüpheli yoğun istek tespit edildi")
            times.append(now)

            # UA boş veya bilinen bot ise engelle
            if not ua or any(bad in ua for bad in _BAD_UA):
                raise HTTPException(status_code=403, detail="Şüpheli istemci tespit edildi")

            # SQLi / XSS gibi basit desenler
            body = await request.body()
            request._body = body
            payload = request.url.path + "?" + request.url.query if request.url.query else request.url.path
            payload += " " + body.decode(errors="ignore")
            if _SUSPICIOUS_RE.search(payload):
                raise HTTPException(status_code=403, detail="Şüpheli içerik tespit edildi")

            return await call_next(request)
        except HTTPException:
            raise
        except Exception:
            return await call_next(request)

async def anomaly_fraud_detect_middleware(request, call_next):
    return await AnomalyFraudDetectMiddleware(None).dispatch(request, call_next)
