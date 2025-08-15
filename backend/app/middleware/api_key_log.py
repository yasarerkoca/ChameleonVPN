from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import HTTPException
from app.models.security.api_key import APIKey
from app.models.security.api_key_access_log import APIKeyAccessLog
from app.utils.db.db_utils import get_db
import datetime
import time

# Basit RAM cache (İsteğe bağlı: Redis ile değiştirilebilir)
API_KEY_RATE_CACHE = {}

class APIKeyAccessLogger(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        db = next(get_db())
        api_key_str = request.headers.get("X-API-KEY")
        now = int(time.time())

        if api_key_str:
            key_obj = db.query(APIKey).filter_by(key=api_key_str).first()
            if key_obj:
                if key_obj.is_blocked:
                    raise HTTPException(status_code=403, detail="API Key is blocked")

                # Dakikalık rate limit
                limit = key_obj.rate_limit_per_minute or 100
                cache_key = f"{api_key_str}:{now // 60}"
                count = API_KEY_RATE_CACHE.get(cache_key, 0)
                if count >= limit:
                    key_obj.is_blocked = True
                    key_obj.last_blocked_at = datetime.datetime.utcnow()
                    db.commit()
                    raise HTTPException(status_code=429, detail="API Key rate limit exceeded")
                API_KEY_RATE_CACHE[cache_key] = count + 1

                # Logla
                log = APIKeyAccessLog(
                    api_key_id=key_obj.id,
                    accessed_at=datetime.datetime.utcnow(),
                    ip_address=request.client.host,
                    endpoint=str(request.url.path),
                    http_method=request.method,
                    status_code=200  # Gerçek response’dan sonra override edilebilir
                )
                db.add(log)
                db.commit()

        response = await call_next(request)
        return response
