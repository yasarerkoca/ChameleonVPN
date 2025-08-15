from sqlalchemy.orm import Session
from app.models.user.user import User


def create_social_user(db: Session, email: str, full_name: str) -> User:
    new_user = User(
        email=email,
        full_name=full_name,
        password_hash=None,
        is_email_verified=True,
        is_active=True,
        is_social_account=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_or_create_social_user(db: Session, email: str, full_name: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    return user if user else create_social_user(db, email, full_name)
