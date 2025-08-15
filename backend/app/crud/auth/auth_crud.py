from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.models.user.user import User


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def update_user_password(db: Session, user: User, hashed_pw: str):
    user.password_hash = hashed_pw
    user.reset_token = None
    user.reset_token_expiration = None
    db.commit()


def set_reset_token(db: Session, user: User, token: Optional[str], expiration_minutes: int = 30):
    user.reset_token = token
    user.reset_token_expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    db.commit()


def verify_user_email(db: Session, user: User):
    user.is_email_verified = True
    db.commit()


def update_last_login(db: Session, user: User):
    user.last_login_at = datetime.utcnow()
    db.commit()
