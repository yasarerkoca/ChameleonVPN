from sqlalchemy.orm import Session
from app.models.user.user import User
from app.schemas.user.user_base import UserCreate, UserUpdate
from app.utils.auth.auth_utils import get_password_hash, verify_password


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        email=user.email,
        full_name=user.full_name,
        password_hash=get_password_hash(user.password),
        is_active=True,
        is_email_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def authenticate_user(db: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user


def update_user_password(db: Session, user: User, new_password: str) -> User:
    user.password_hash = get_password_hash(new_password)
    db.commit()
    db.refresh(user)
    return user


def update_user_info(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def set_reset_token(db: Session, user: User, token: str) -> None:
    user.reset_token = token
    db.commit()
