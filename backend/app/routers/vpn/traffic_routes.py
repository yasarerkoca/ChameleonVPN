from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.vpn.vpn_log import VPNLog
from app.schemas.vpn.vpn_log import VPNLogOut

router = APIRouter(
    prefix="/vpn/traffic",
    tags=["vpn-traffic"]
)

@router.get("/my", response_model=List[VPNLogOut], summary="Kendi trafik loglarımı getir")
def my_traffic_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Giriş yapan kullanıcının kendi trafik loglarını listeler.
    """
    return db.query(VPNLog)\
        .filter(VPNLog.user_id == current_user.id)\
        .order_by(VPNLog.timestamp.desc())\
        .all()

@router.get("/all", response_model=List[VPNLogOut], summary="Tüm kullanıcıların trafik loglarını getir (admin)")
def all_traffic_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Sadece admin kullanıcısı için tüm trafik loglarını döner.
    """
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return db.query(VPNLog).order_by(VPNLog.timestamp.desc()).all()
