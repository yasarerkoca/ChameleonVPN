from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.schemas.vpn.vpn_connection_history import VPNConnectionHistoryCreate, VPNConnectionHistoryOut
from app.crud.vpn.vpn_connection_history_crud import create_vpn_connection_log, get_user_vpn_history

router = APIRouter(
    prefix="/vpn/connection",
    tags=["vpn-connection"]
)

@router.post("/", response_model=VPNConnectionHistoryOut, summary="VPN bağlantı geçmişi kaydet")
def log_connection(
    log_data: VPNConnectionHistoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if log_data.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Başka kullanıcı için log eklenemez")
    return create_vpn_connection_log(db, log_data)

@router.get("/me", response_model=List[VPNConnectionHistoryOut], summary="Kendi bağlantı geçmişini getir")
def get_my_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_vpn_history(db, current_user.id)
