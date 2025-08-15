from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.vpn.vpn_server import VPNServer
from app.models.user.user_session import UserSession
from app.schemas.vpn.vpn_server import VPNServerOut
from app.schemas.user.user_session import UserSessionOut

router = APIRouter(
    prefix="/vpn/status",
    tags=["vpn-status"]
)

@router.get("/servers", response_model=List[VPNServerOut], summary="Tüm VPN sunucularının durumunu getir")
def list_server_status(db: Session = Depends(get_db)):
    """
    Tüm VPN sunucularının (ör: aktif, pasif, yük durumu) temel durum bilgisini döndürür.
    """
    # Not: Sunucu modeli üzerinde status, load, last_heartbeat vs. alanlar olmalı.
    return db.query(VPNServer).all()

@router.get("/sessions", response_model=List[UserSessionOut], summary="Tüm aktif kullanıcı oturumlarını getir (admin)")
def list_active_sessions(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Sadece admin görebilsin:
    if not getattr(current_user, "is_admin", False):
        return []
    return db.query(UserSession).filter(UserSession.status == "active").all()
