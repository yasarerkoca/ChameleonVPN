from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.corporate.corporate_user_group import CorporateUserGroup
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory
from app.models.user.user import User
from app.utils.db.db_utils import get_db
from app.deps import require_role

router = APIRouter(
    prefix="/admin/corporate-groups",
    tags=["admin-corporate-groups"]
)

@router.get("/", summary="Tüm kurumsal grupları listele")
def list_corporate_groups(db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    return db.query(CorporateUserGroup).all()

@router.get("/{group_id}/users", summary="Gruba ait kullanıcıları getir")
def group_users(group_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    group = db.query(CorporateUserGroup).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.users

@router.post("/assign/{user_id}/{group_id}", summary="Kullanıcıyı gruba ata")
def assign_user_group(user_id: int, group_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_role("admin"))):
    user = db.query(User).get(user_id)
    group = db.query(CorporateUserGroup).get(group_id)
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or Group not found")

    old_value = str(user.corporate_group_id) if user.corporate_group_id else "None"
    user.corporate_group_id = group_id
    db.commit()

    db.add(CorporateUserRightsHistory(
        user_id=user.id,
        changed_by_admin_id=current_user.id,
        field_changed="corporate_group_id",
        old_value=old_value,
        new_value=str(group_id),
        note=f"{group.name} grubuna atandı"
    ))
    db.commit()

    return {"msg": f"{user.email} kullanıcısı {group.name} grubuna atandı."}
