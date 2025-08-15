from sqlalchemy.orm import Session
from app.models.user.user_external_auth import UserExternalAuth
from app.schemas.user.user_meta import ExternalAuthCreate


def create_external_auth(db: Session, auth_data: ExternalAuthCreate) -> UserExternalAuth:
    auth = UserExternalAuth(**auth_data.dict())
    db.add(auth)
    db.commit()
    db.refresh(auth)
    return auth


def get_external_auth_by_provider(db: Session, provider: str, provider_user_id: str) -> UserExternalAuth | None:
    return db.query(UserExternalAuth).filter(
        UserExternalAuth.provider == provider,
        UserExternalAuth.provider_user_id == provider_user_id
    ).first()


def get_external_auth_by_user(db: Session, user_id: int) -> list[UserExternalAuth]:
    return db.query(UserExternalAuth).filter(UserExternalAuth.user_id == user_id).all()
