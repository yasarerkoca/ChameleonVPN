from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.schemas.proxy.proxy_out import ProxyOut, ProxyQuotaOut, ProxyPurchaseRequest, ProxyLogOut
from app.crud.proxy.proxy_crud import (
    get_user_proxies,
    get_proxy_quota_status,
    purchase_proxy,
    get_proxy_logs
)

router = APIRouter(
    prefix="/proxy",
    tags=["proxy-user"]
)

@router.get("/list", response_model=List[ProxyOut], summary="Kullanıcının sahip olduğu proxy IP'leri")
def list_user_proxies(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_user_proxies(db, current_user.id)

@router.get("/quota", response_model=ProxyQuotaOut, summary="Kullanıcının mevcut proxy kotasını getir")
def get_proxy_quota(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_proxy_quota_status(db, current_user.id)

@router.post("/purchase", response_model=ProxyOut, summary="Proxy satın al (veya ata)")
def purchase_proxy_endpoint(
    request: ProxyPurchaseRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return purchase_proxy(db, current_user.id, request.proxy_id)

@router.get("/logs", response_model=List[ProxyLogOut], summary="Kullanıcıya ait proxy kullanım loglarını getir")
def list_proxy_logs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_proxy_logs(db, current_user.id)
