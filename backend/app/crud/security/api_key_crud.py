from sqlalchemy.orm import Session
from app.models.security.api_key import APIKey


def get_api_key_by_key(db: Session, key: str):
    return db.query(APIKey).filter(APIKey.key == key).first()


def create_api_key(db: Session, api_key: APIKey):
    db.add(api_key)
    db.commit()
    db.refresh(api_key)
    return api_key


def revoke_api_key(db: Session, key: str):
    api_key = get_api_key_by_key(db, key)
    if api_key:
        api_key.revoked = True
        db.commit()
    return api_key
