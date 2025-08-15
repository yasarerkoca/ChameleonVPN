# ~/ChameleonVPN/backend/app/models/user/user.py

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from app.config.database import Base
from app.models.corporate import CorporateUserGroup
from app.models.security.limit import UserLimit  # Limit modeli

class User(Base):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(128), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=True)
    full_name = Column(String(128), nullable=True)
    is_active = Column(Boolean, default=True)
    is_email_verified = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)
    role = Column(String(16), default="user")
    status = Column(String(16), default="active")

    corporate_account_id = Column(Integer, nullable=True)
    is_corporate_admin = Column(Boolean, default=False)
    corporate_group_id = Column(Integer, ForeignKey("corporate_user_groups.id"), nullable=True)

    mfa_enabled = Column(Boolean, default=False)
    totp_secret = Column(String(32), nullable=True)

    last_login = Column(DateTime, nullable=True)
    last_ip = Column(String(64), nullable=True)
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    referral_code = Column(String(16), unique=True, nullable=True)
    referred_by = Column(String(16), nullable=True)

    notification_settings = Column(JSONB, nullable=True)
    flags = Column(JSONB, nullable=True)
    preferences = Column(JSONB, nullable=True)
    preferred_language = Column(String(8), default="tr")
    phone_number = Column(String(32), nullable=True)

    country_code = Column(String(8), nullable=True)
    city = Column(String(64), nullable=True)
    region = Column(String(64), nullable=True)

    reset_token = Column(String(256), nullable=True)
    reset_token_expire = Column(DateTime, nullable=True)
    is_deleted = Column(Boolean, default=False)
    anonymized_at = Column(DateTime, nullable=True)

    proxy_quota_gb = Column(Integer, default=0)
    active_proxy_count = Column(Integer, default=0)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)

    # İlişkiler
    limits = relationship("UserLimit", back_populates="user", cascade="all, delete-orphan")
    corporate_group = relationship("CorporateUserGroup", back_populates="users", foreign_keys=[corporate_group_id])
    notifications = relationship("UserNotification", back_populates="user", cascade="all, delete-orphan")
    relationships = relationship("UserRelationship", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User id={self.id} email={self.email} active={self.is_active}>"

# --- REL PATCH (auto) ---
from sqlalchemy.orm import relationship
try:
    from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory  # noqa
except Exception:
    pass
else:
    try:
        User  # noqa
        if not hasattr(User, "corporate_rights_changes"):
            User.corporate_rights_changes = relationship(
                "CorporateUserRightsHistory",
                back_populates="user",
                cascade="all, delete-orphan",
            )
    except NameError:
        pass
# --- /REL PATCH ---


# --- AUTO PATCH: relationships ---
try:
    User  # noqa
    if not hasattr(User, "api_keys"):
        api_keys = relationship(
            "APIKey",
            back_populates="user",
            cascade="all, delete-orphan",
        )
        User.api_keys = api_keys
except NameError:
    pass
# --- END PATCH ---
