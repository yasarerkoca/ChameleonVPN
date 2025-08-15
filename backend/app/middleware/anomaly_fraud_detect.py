SKIP_PATHS={"/docs","/openapi.json","/redoc","/metrics"}
# ~/ChameleonVPN/backend/app/middleware/anomaly_fraud_detect.py

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.db.db_utils import get_db
from app.models.user.user_session import UserSession
from app.crud.logs.anomaly_fraud_record_crud import log_anomaly

class AnomalyFraudDetectMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            # Sadece login/session-required endpointlerde çalışacak şekilde gerekirse kontrol ekle
            user = getattr(request.state, "user", None)
            db = next(get_db())
            client_ip = request.client.host
            if user and user.id:
                # 1- Aynı kullanıcı kısa sürede farklı IP ile giriş yaparsa
                recent_sessions = db.query(UserSession).filter(
                    UserSession.user_id == user.id
                ).order_by(UserSession.login_time.desc()).limit(5).all()
                if recent_sessions and recent_sessions[0].ip_address != client_ip:
                    log_anomaly(
                        db=db,
                        user_id=user.id,
                        ip_address=client_ip,
                        reason="IP değişikliği",
                        details=f"Son giriş IP: {recent_sessions[0].ip_address}, Şimdi: {client_ip}"
                    )
                # 2- Aynı IP'den çok fazla farklı hesap denemesi (ör: 5'ten fazla)
                unique_users = db.query(UserSession.user_id).filter(
                    UserSession.ip_address == client_ip
                ).distinct().count()
                if unique_users > 5:
                    log_anomaly(
                        db=db,
                        user_id=user.id,
                        ip_address=client_ip,
                        reason="Çoklu kullanıcı denemesi",
                        details=f"Aynı IP ile {unique_users} farklı kullanıcı denemesi"
                    )
                # 3- Aynı anda 3'ten fazla aktif oturum (parallel login)
                active_sessions = db.query(UserSession).filter(
                    UserSession.user_id == user.id,
                    UserSession.logout_time.is_(None)
                ).count()
                if active_sessions > 3:
                    log_anomaly(
                        db=db,
                        user_id=user.id,
                        ip_address=client_ip,
                        reason="Çoklu aktif oturum",
                        details=f"Aynı anda {active_sessions} aktif oturum tespit edildi"
                    )
        except Exception:
            pass
        
    if request.url.path in SKIP_PATHS:
        return await call_next(request)
    return await call_next(request)

