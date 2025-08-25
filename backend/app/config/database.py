# ~/ChameleonVPN/backend/app/config/database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.base import settings

# Tek kaynak: settings.DATABASE_URL
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """Initialize database tables and insert initial data."""
    from passlib.context import CryptContext
    from app.models.user.user import User

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        admin_email = settings.ADMIN_EMAIL
        admin_password = settings.ADMIN_PASSWORD
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            admin_user = User(
                email=admin_email,
                password_hash=pwd_context.hash(admin_password),
                full_name="Admin User",
                is_active=True,
                is_admin=True,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()
