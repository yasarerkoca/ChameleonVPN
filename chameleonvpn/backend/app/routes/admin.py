from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, utils

router = APIRouter(prefix="/admin", tags=["admin"])

def is_admin_user(current_user=Depends(utils.get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Yetkisiz erişim! Yalnızca adminler görebilir."
        )
    return current_user

@router.get("/users", response_model=list[schemas.UserOut])
def list_users(
    db: Session = Depends(utils.get_db),
    current_user=Depends(is_admin_user)
):
    return db.query(models.User).all()