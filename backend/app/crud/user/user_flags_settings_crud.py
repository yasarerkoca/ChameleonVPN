from sqlalchemy.orm import Session
from app.models.user.user_flags_settings import UserFlagsSettings
from app.schemas.user.user_meta import UserFlagsUpdate


def get_flags_by_user_id(db: Session, user_id: int) -> UserFlagsSettings | None:
    return db.query(UserFlagsSettings).filter(UserFlagsSettings.user_id == user_id).first()


def update_user_flags(db: Session, user_id: int, flags_update: UserFlagsUpdate) -> UserFlagsSettings:
    flags = get_flags_by_user_id(db, user_id)
    if not flags:
        flags = UserFlagsSettings(user_id=user_id)

    for key, value in flags_update.dict(exclude_unset=True).items():
        setattr(flags, key, value)

    db.add(flags)
    db.commit()
    db.refresh(flags)
    return flags
