"""Initial database seed for admin user and roles."""
from sqlalchemy import text
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.config.database import Base, engine, SessionLocal
from app.models.user.user import User
import json

DEFAULT_ROLES = [
    {"name": "admin", "permissions": ["*"]},
    {"name": "user", "permissions": []},
]

def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    try:
        for role in DEFAULT_ROLES:
            db.execute(
                text(
                    "INSERT INTO roles (name, permissions) VALUES (:name, :permissions) "
                    "ON CONFLICT(name) DO NOTHING"
                ),
                {
                    "name": role["name"],
                    "permissions": json.dumps(role["permissions"]),
                },
            )
        admin_email = "admin@example.com"
        admin = db.query(User).filter(User.email == admin_email).first()
        if not admin:
            admin_user = User(
                email=admin_email,
                password_hash=pwd_context.hash("admin"),
                full_name="Admin User",
                is_active=True,
                is_admin=True,
                role="admin",
            )
            db.add(admin_user)
        db.commit()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
