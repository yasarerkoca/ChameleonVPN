# ~/ChameleonVPN/backend/app/models/security/two_factor_tokens.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class TwoFactorToken(Base):
    __tablename__ = "two_factor_tokens"
    __table_args__ = (
        Index("ix_two_factor_user_id", "user_id"),
        Index("ix_two_factor_expires_at", "expires_at"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    token = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # User tarafında: two_factor_tokens = relationship("TwoFactorToken", back_populates="user", cascade="all, delete-orphan")
    user = relationship("User", back_populates="two_factor_tokens", passive_deletes=True)

    def __repr__(self):
        return f"<TwoFactorToken id={self.id} user_id={self.user_id} expires_at={self.expires_at}>"
