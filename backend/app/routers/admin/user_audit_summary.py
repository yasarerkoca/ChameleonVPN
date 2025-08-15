from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user.user import User
from app.models.user.user_notification import UserNotification
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.models.logs.user_manual_audit import UserManualAudit
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional

router = APIRouter(
    prefix="/admin/audit-summary",
    tags=["admin-audit-summary"]
)

def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

@router.get("/user/{user_id}", summary="Kullanıcının tüm geçmiş denetim kayıtlarını getir")
def user_full_audit_summary(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    notifs = db.query(UserNotification).filter(UserNotification.user_id == user_id).all()
    status_logs = db.query(CorporateUserRightsHistory).filter(CorporateUserRightsHistory.user_id == user_id).all()
    manual_audits = db.query(UserManualAudit).filter(UserManualAudit.user_id == user_id).all()
    return {
        "notifications": notifs,
        "status_history": status_logs,
        "manual_audits": manual_audits
    }
