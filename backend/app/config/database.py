from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config.base import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=10, max_overflow=20, pool_timeout=30)
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

    # Create tables based on the SQLAlchemy models
    Base.metadata.create_all(bind=engine)

    # Prepare a database session for inserting initial data
    db = SessionLocal()
    try:
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        # Create a default admin user if it does not exist
        admin_email = "admin@example.com"
        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if not existing_admin:
            admin_user = User(
                email=admin_email,
                password_hash=pwd_context.hash("admin"),
                full_name="Admin User",
                is_active=True,
                is_admin=True,
            )
            db.add(admin_user)
            db.commit()
    finally:
        db.close()
