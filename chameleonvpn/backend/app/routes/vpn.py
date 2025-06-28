from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas, utils

router = APIRouter(prefix="/vpn", tags=["vpn"])

@router.get("/profiles", response_model=list[schemas.VPNProfileOut])
def list_profiles(
    db: Session = Depends(utils.get_db),
    current_user=Depends(utils.get_current_user)
):
    return db.query(models.VPNProfile).filter(models.VPNProfile.user_id == current_user.id).all()

@router.post("/profiles", response_model=schemas.VPNProfileOut)
def create_profile(
    profile: schemas.VPNProfileCreate,
    db: Session = Depends(utils.get_db),
    current_user=Depends(utils.get_current_user)
):
    db_profile = models.VPNProfile(user_id=current_user.id, **profile.dict())
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile