# ~/ChameleonVPN/backend/app/models/security/two_factor_tokens.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base


class TwoFactorToken(Base):
    __tablename__ = "two_factor_tokens"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    token = Column(String(64), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)

    user = relationship("User", back_populates="two_factor_tokens")

    def __repr__(self):
        return f"<TwoFactorToken user_id={self.user_id}, expires_at={self.expires_at}>"

