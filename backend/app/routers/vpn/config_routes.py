from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.schemas.vpn.vpn_config import VPNConfigOut
from app.crud.vpn.config_crud import (
    get_vpn_config_for_user,
    get_all_vpn_configs
)

router = APIRouter(
    prefix="/vpn/config",
    tags=["vpn-config"]
)

@router.get("/my", response_model=VPNConfigOut, summary="Kullanıcının aktif VPN yapılandırmasını getir")
def get_my_vpn_config(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    config = get_vpn_config_for_user(db, current_user.id)
    if not config:
        raise HTTPException(status_code=404, detail="Active VPN config not found")
    return config

@router.get("/all", response_model=List[VPNConfigOut], summary="Tüm kullanıcıların aktif VPN yapılandırmalarını getir (admin)")
def get_all_vpn_configs_endpoint(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return get_all_vpn_configs(db)
