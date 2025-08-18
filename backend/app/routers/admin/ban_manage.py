from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user

router = APIRouter(
    prefix="/admin/user-control",
    tags=["admin-user-control"]
)

def admin_required(current_user: User = Depends(get_current_user)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

@router.post("/ban/{user_id}", summary="Kullanıcıyı banla")
def ban_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = 'banned'
    user.is_active = False
    db.commit()

    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=current_user.id,
        field_changed="status",
        old_value="active",
        new_value="banned",
        note="Admin tarafından banlandı"
    ))
    db.commit()

    return {"msg": f"{user.email} kullanıcısı banlandı."}

@router.post("/unban/{user_id}", summary="Kullanıcının banını kaldır")
def unban_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(admin_required)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = 'active'
    user.is_active = True
    db.commit()

    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=current_user.id,
        field_changed="status",
        old_value="banned",
        new_value="active",
        note="Admin tarafından ban kaldırıldı"
    ))
    db.commit()

    return {"msg": f"{user.email} kullanıcısının banı kaldırıldı."}

@router.post("/quarantine/{user_id}", summary="Kullanıcıyı karantinaya al")
def quarantine_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "quarantined"
    user.is_active = False
    db.commit()
    return {"msg": f"{user.email} karantinaya alındı."}

@router.get("/quarantined", summary="Karantinaya alınmış kullanıcıları listele")
def list_quarantined_users(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(User).filter(User.status == "quarantined").all()

@router.post("/rehabilitate/{user_id}", summary="Karantinadaki kullanıcıyı aktifleştir")
def rehabilitate_user(user_id: int, db: Session = Depends(get_db), _: User = Depends(admin_required)):
    user = db.query(User).get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.status = "active"
    user.is_active = True
    db.commit()
    return {"msg": f"{user.email} tekrar aktifleştirildi."}
