SKIP_PATHS={"/docs","/openapi.json","/redoc","/metrics"}
# ~/ChameleonVPN/backend/app/middleware/session_hijack.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.db.db_utils import get_db
from app.models.user.user_session import UserSession
from app.crud.logs.anomaly_fraud_record_crud import log_anomaly
from app.utils.token.token_utils import decode_access_token

class SessionHijackMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Sadece JWT korumalı endpointlerde çalışsın (örn: /auth hariç)
        if request.url.path.startswith("/auth"):
            
    if request.url.path in SKIP_PATHS:
        return await call_next(request)
    return await call_next(request)

        # JWT token al
        auth = request.headers.get("authorization")
        if not auth or not auth.lower().startswith("bearer "):
            return await call_next(request)
        token = auth.split()[1]
        try:
            payload = decode_access_token(token)
            session_id = payload.get("session_id")
            user_id = payload.get("user_id")
            ip = request.client.host
            agent = request.headers.get("user-agent", "")
            db = next(get_db())
            if session_id:
                session = db.query(UserSession).filter_by(id=session_id, user_id=user_id).first()
                if session and session.ip_address != ip:
                    # Farklı IP ile kullanım, anomaly logla
                    create_anomaly_log(
                        db=db,
                        user_id=user_id,
                        type="session_hijack",
                        details=f"Token başka IP'den kullanıldı! Orijinal: {session.ip_address}, Şimdi: {ip}, UA: {agent}",
                        status="detected"
                    )
        except Exception:
            pass
        return await call_next(request)
