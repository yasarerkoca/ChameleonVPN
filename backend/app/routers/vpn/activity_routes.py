from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.user.user_server_activity import UserServerActivity
from app.schemas.user.user_activity import UserServerActivityOut
from app.deps import require_role

router = APIRouter(
    prefix="/vpn/activity",
    tags=["vpn-activity"]
)

@router.get("/my", response_model=List[UserServerActivityOut], summary="Kendi VPN bağlantı geçmişimi getir")
def my_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(UserServerActivity)\
        .filter(UserServerActivity.user_id == current_user.id)\
        .order_by(UserServerActivity.timestamp.desc()).all()

@router.get("/all", response_model=List[UserServerActivityOut], summary="Tüm kullanıcıların VPN aktivite loglarını getir (admin)")
def all_activity(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    return db.query(UserServerActivity)\
        .order_by(UserServerActivity.timestamp.desc()).all()
