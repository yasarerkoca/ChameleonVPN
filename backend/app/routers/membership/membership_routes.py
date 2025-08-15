from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.schemas.payment.plan_base import PlanOut
from app.schemas.membership.membership_out import MembershipOut
from app.schemas.membership.subscribe_request import SubscribeRequest
from app.schemas.membership.upgrade_request import UpgradeRequest
from app.schemas.quota.quota_out import QuotaUsageOut
from app.crud.payment.membership_crud import (  # GÜNCELLENDİ
    get_all_plans,
    get_plan_by_id,
    create_membership,
    get_active_membership,
    get_quota_status,
    upgrade_membership,
    cancel_membership as cancel_user_membership
)
from app.models.user.user import User

router = APIRouter(
    prefix="/membership",
    tags=["membership"]
)

@router.get("/plan-list", response_model=List[PlanOut], summary="Tüm abonelik planlarını listele")
def get_plan_list(db: Session = Depends(get_db)):
    return get_all_plans(db)

@router.post("/subscribe", response_model=MembershipOut, summary="Seçilen plana abone ol")
def subscribe_to_plan(
    data: SubscribeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    plan = get_plan_by_id(db, data.plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return create_membership(db, current_user, plan)

@router.get("/current", response_model=MembershipOut, summary="Aktif aboneliği görüntüle")
def get_current_membership(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_active_membership(db, current_user.id)

@router.get("/usage", response_model=QuotaUsageOut, summary="Kota kullanım bilgisini getir")
def get_quota_info(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_quota_status(db, current_user.id)

@router.post("/upgrade", response_model=MembershipOut, summary="Abonelik yükselt (upgrade)")
def upgrade_plan(
    data: UpgradeRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return upgrade_membership(db, current_user, data.new_plan_id)

@router.post("/cancel", summary="Aboneliği iptal et")
def cancel_current_membership(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cancel_user_membership(db, current_user.id)
    return {"detail": "Membership cancelled"}
