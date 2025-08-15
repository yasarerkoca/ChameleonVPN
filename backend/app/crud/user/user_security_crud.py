from sqlalchemy.orm import Session
from app.models.user.user_security import UserSecurity
from app.schemas.user.user_meta import UserSecurityUpdate


def get_user_security(db: Session, user_id: int) -> UserSecurity | None:
    return db.query(UserSecurity).filter(UserSecurity.user_id == user_id).first()


def update_user_security(db: Session, user_id: int, data: UserSecurityUpdate) -> UserSecurity:
    security = get_user_security(db, user_id)
    if not security:
        security = UserSecurity(user_id=user_id)
        db.add(security)

    for key, value in data.dict(exclude_unset=True).items():
        setattr(security, key, value)

    db.commit()
    db.refresh(security)
    return security
