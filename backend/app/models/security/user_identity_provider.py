# ~/ChameleonVPN/backend/app/models/security/user_identity_provider.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.sql import func
from app.config.database import Base

class UserIdentityProvider(Base):
    __tablename__ = "user_identity_providers"
    __table_args__ = (
        UniqueConstraint("provider", "provider_uid", name="uq_provider_uid"),
        Index("ix_uip_user_id", "user_id"),
        Index("ix_uip_provider", "provider"),
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    provider = Column(String(50), nullable=False)         # ör: google.com, apple.com
    provider_uid = Column(String(255), nullable=False)    # Firebase uid / sub
    email = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
