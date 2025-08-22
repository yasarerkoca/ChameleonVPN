# ~/ChameleonVPN/backend/app/crud/security/identity_provider_crud.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.security.user_identity_provider import UserIdentityProvider

def get_by_provider_uid(db: Session, provider: str, provider_uid: str):
    stmt = select(UserIdentityProvider).where(
        UserIdentityProvider.provider == provider,
        UserIdentityProvider.provider_uid == provider_uid
    )
    return db.execute(stmt).scalar_one_or_none()

def link_user_provider(db: Session, user_id: int, provider: str, provider_uid: str, email: str | None):
    item = UserIdentityProvider(user_id=user_id, provider=provider, provider_uid=provider_uid, email=email)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
