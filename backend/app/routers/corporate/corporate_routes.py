from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.models.corporate.corporate_user_group import CorporateUserGroup
from app.models.user.user import User
from app.schemas.corporate.corporate_user_group import (
    CorporateUserGroupCreate,
    CorporateUserGroupOut
)

router = APIRouter(
    prefix="/admin/corporate-groups",
    tags=["admin-corporate-groups"]
)

@router.post("/", response_model=CorporateUserGroupOut, summary="Yeni kurumsal grup oluştur")
def create_corporate_group(
    group: CorporateUserGroupCreate,
    db: Session = Depends(get_db)
):
    db_group = CorporateUserGroup(name=group.name, max_proxies=group.max_proxies)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/", response_model=List[CorporateUserGroupOut], summary="Kurumsal grupları listele")
def list_corporate_groups(db: Session = Depends(get_db)):
    return db.query(CorporateUserGroup).all()

@router.put("/user/{user_id}/assign/{group_id}", summary="Kullanıcıyı kurumsal gruba ata")
def assign_user_to_group(
    user_id: int,
    group_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    group = db.query(CorporateUserGroup).filter(CorporateUserGroup.id == group_id).first()
    if not user or not group:
        raise HTTPException(status_code=404, detail="User or group not found")
    user.corporate_group_id = group_id
    db.commit()
    return {"msg": f"{user.email} kullanıcısı {group.name} grubuna atandı."}

@router.get("/{group_id}/users", summary="Gruba atanmış kullanıcıları getir")
def list_group_users(
    group_id: int,
    db: Session = Depends(get_db)
):
    group = db.query(CorporateUserGroup).filter(CorporateUserGroup.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    return group.users
