from sqlalchemy.orm import Session
from app.models.security.refresh_token_blacklist import RefreshTokenBlacklist

def blacklist_token(db: Session, token: str, reason: str = ""):
    entry = RefreshTokenBlacklist(token=token, reason=reason)
    db.add(entry)
    db.commit()

def is_token_blacklisted(db: Session, token: str) -> bool:
    return db.query(RefreshTokenBlacklist).filter_by(token=token).first() is not None
