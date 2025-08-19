from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.models.user.user_session import UserSession
from app.deps import require_role

router = APIRouter(
    prefix="/admin/session-management",
    tags=["admin-session-management"]
)

@router.get("/active", summary="Tüm aktif oturumları getir")
def list_active_sessions(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(UserSession).filter(UserSession.status == 'active').all()

@router.get("/user/{user_id}", summary="Kullanıcının tüm oturum geçmişini getir")
def user_sessions(user_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(UserSession).filter_by(user_id=user_id).order_by(UserSession.started_at.desc()).all()

@router.post("/end/{session_id}", summary="Belirli bir oturumu sonlandır")
def end_session(session_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    session = db.query(UserSession).get(session_id)
    if not session or session.status != 'active':
        raise HTTPException(status_code=404, detail="Active session not found")
    session.status = 'ended'
    session.ended_at = datetime.utcnow()
    db.commit()
    return {"msg": "Session ended."}

@router.post("/end-all", summary="Tüm aktif oturumları sonlandır")
def end_all_sessions(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    sessions = db.query(UserSession).filter(UserSession.status == 'active').all()
    for session in sessions:
        session.status = 'ended'
        session.ended_at = datetime.utcnow()
    db.commit()
    return {"msg": f"Tüm aktif oturumlar sonlandırıldı. Toplam: {len(sessions)}"}
