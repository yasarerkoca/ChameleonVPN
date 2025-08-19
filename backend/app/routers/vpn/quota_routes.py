from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.security.limit import UserLimit
from app.schemas.quota.quota_out import UserLimitOut
from app.deps import require_role

router = APIRouter(
    prefix="/vpn/quota",
    tags=["vpn-quota"]
)

@router.get("/my", response_model=UserLimitOut, summary="Kendi VPN kotamı getir")
def my_quota(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    quota = db.query(UserLimit).filter(UserLimit.user_id == current_user.id).first()
    if not quota:
        raise HTTPException(status_code=404, detail="Quota not set")
    return quota

@router.get("/all", response_model=List[UserLimitOut], summary="Tüm kullanıcıların VPN kotasını getir (admin)")
def all_quotas(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return db.query(UserLimit).all()
