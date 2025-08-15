from sqlalchemy.orm import Session
from app.models.user.user_profile import UserProfile
from app.schemas.user.user_meta import UserProfileUpdate
from typing import Optional


def get_user_profile(db: Session, user_id: int) -> Optional[UserProfile]:
    return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()


def update_user_profile(db: Session, user_id: int, data: UserProfileUpdate) -> UserProfile:
    profile = get_user_profile(db, user_id)
    if not profile:
        profile = UserProfile(user_id=user_id)
        db.add(profile)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile
