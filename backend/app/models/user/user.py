# ~/ChameleonVPN/backend/app/models/user/user.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.config.database import Base
from app.models.role import Role, user_roles
from app.models.permission import Permission, user_permissions

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

    # ---------------------------
    # İlişkiler (back_populates)
    # ---------------------------

    # Kurumsal grup (N:1)
    corporate_group = relationship(
        "CorporateUserGroup",
        back_populates="users",
        foreign_keys=[corporate_group_id],
    )

    # Limitler (1:N)
    limits = relationship(
        "UserLimit",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Bildirimler (1:N)
    notifications = relationship(
        "UserNotification",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Kullanıcı ilişkileri — ÇIKIŞ (user_id)
    relationships = relationship(
        "UserRelationship",
        foreign_keys="[UserRelationship.user_id]",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Kullanıcı ilişkileri — GİRİŞ (related_user_id)
    related_relationships = relationship(
        "UserRelationship",
        foreign_keys="[UserRelationship.related_user_id]",
        back_populates="related_user",
        cascade="all, delete-orphan",
    )

    # API anahtarları (1:N)
    api_keys = relationship(
        "APIKey",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # 2FA tokenları (1:N)
    two_factor_tokens = relationship(
        "TwoFactorToken",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # Kurumsal hak değişikliği geçmişi (1:N) — CorporateUserRightsHistory.user
    corporate_rights_history = relationship(
        "CorporateUserRightsHistory",
        back_populates="user",
        cascade="all, delete-orphan",
        foreign_keys="CorporateUserRightsHistory.user_id",
    )

    # Admin tarafından yapılan değişiklikler (1:N) — CorporateUserRightsHistory.changed_by_admin
    admin_rights_changes = relationship(
        "CorporateUserRightsHistory",
        back_populates="changed_by_admin",
        cascade="all, delete-orphan",
        foreign_keys="CorporateUserRightsHistory.changed_by_admin_id",
    )

    # RBAC relationships
    roles = relationship("Role", secondary=user_roles, back_populates="users")
    permissions = relationship(
        "Permission", secondary=user_permissions, back_populates="users"
    )

    def __repr__(self):
        return f"<User id={self.id} email={self.email} active={self.is_active}>"
