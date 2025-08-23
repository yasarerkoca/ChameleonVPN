
import re
from fastapi import HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

import redis.asyncio as aioredis
from redis.exceptions import RedisError

from .common import should_bypass
from app.config.base import settings

# Redis tabanlı istek sayacı. Bağlantı `dispatch` içerisinde oluşturulur.
_REQUEST_STORE = None

logger = logging.getLogger(__name__)

# Şüpheli UA ve payload desenleri
_BAD_UA = ("curl", "bot", "crawler", "scan")
_SUSPICIOUS_RE = re.compile(r"(union select|drop table|or 1=1|<script)", re.IGNORECASE)
_MAX_PER_MINUTE = 100

_RATE_LIMIT_LUA = """
local current = redis.call('incr', KEYS[1])
if current == 1 then
  redis.call('expire', KEYS[1], ARGV[1])
end
return current
"""

class AnomalyFraudDetectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if should_bypass(request):
            return await call_next(request)
        global _REQUEST_STORE
        if _REQUEST_STORE is None:
            try:
                _REQUEST_STORE = aioredis.from_url(
                    settings.REDIS_URL, encoding="utf-8", decode_responses=True
                )
            except RedisError as exc:
                logger.warning("Redis bağlantısı kurulamadı: %s", exc)
                return await call_next(request)
        try:
            # IP ve UA bilgilerini al
            xff = request.headers.get("x-forwarded-for", "")
            client_ip = (xff.split(",")[0].strip() if xff else None) or (
                request.client.host if request.client else "0.0.0.0"
            )
            ua = request.headers.get("user-agent", "").lower()

            # Basit rate limit kontrolü (Redis üstünde atomik sayaç)
            key = f"af:req:{client_ip}"
            count = await _REQUEST_STORE.eval(_RATE_LIMIT_LUA, 1, key, 60)
            if int(count) > _MAX_PER_MINUTE:
                raise HTTPException(
                    status_code=429, detail="Şüpheli yoğun istek tespit edildi"
                )

            # UA boş veya bilinen bot ise engelle
            if not ua or any(bad in ua for bad in _BAD_UA):
                raise HTTPException(status_code=403, detail="Şüpheli istemci tespit edildi")

            # SQLi / XSS gibi basit desenler
            body = await request.body()
            request._body = body
            payload = (
                request.url.path + "?" + request.url.query
                if request.url.query
                else request.url.path
            )
            payload += " " + body.decode(errors="ignore")
            if _SUSPICIOUS_RE.search(payload):
                raise HTTPException(status_code=403, detail="Şüpheli içerik tespit edildi")

            return await call_next(request)
        except HTTPException:
            raise
        except RedisError as exc:
            logger.warning("Redis hatası: %s", exc)
            return await call_next(request)
        except Exception as exc:
            logger.exception("Beklenmeyen hata", exc_info=exc)
            raise HTTPException(status_code=500) from exc

async def anomaly_fraud_detect_middleware(request, call_next):
    return await AnomalyFraudDetectMiddleware(None).dispatch(request, call_next)
