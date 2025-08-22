from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, Field

from app.models.user.user import User
from app.logs.user_manual_audit import UserManualAudit
from app.utils.db.db_utils import get_db
from app.deps import require_role

router = APIRouter(
    prefix="/admin/manual-audit",
    tags=["admin-manual-audit"]
)

class ManualAuditRequest(BaseModel):
    decision: str = Field(..., example="approve", description="Denetim kararı (ör. approve/reject)")
    notes: Optional[str] = Field("", example="Sebep: Kural ihlali tespit edilmedi.")

@router.post("/{user_id}", summary="Kullanıcıya manuel audit uygula")
def manual_audit(
    user_id: int,
    payload: ManualAuditRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_role("admin"))
):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.add(UserManualAudit(
        user_id=user_id,
        admin_id=current_user.id,
        decision=payload.decision,
        notes=payload.notes
    ))
    db.commit()
    return {"msg": f"Manuel denetim kaydı eklendi: {payload.decision}"}

@router.get("/history/{user_id}", summary="Kullanıcının manuel denetim geçmişi")
def manual_audit_history(
    user_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    return db.query(UserManualAudit)\
        .filter(UserManualAudit.user_id == user_id)\
        .order_by(UserManualAudit.created_at.desc()).all()
