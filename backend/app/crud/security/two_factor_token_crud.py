from sqlalchemy.orm import Session
from app.models.security.two_factor_tokens import TwoFactorToken
from datetime import datetime


def create_2fa_token(db: Session, token: TwoFactorToken):
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def get_valid_2fa_token(db: Session, user_id: int, code: str):
    return db.query(TwoFactorToken).filter(
        TwoFactorToken.user_id == user_id,
        TwoFactorToken.code == code,
        TwoFactorToken.expires_at > datetime.utcnow()
    ).first()
