# ~/ChameleonVPN/backend/app/models/billing/membership.py

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Membership(Base):
    __tablename__ = "membership"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id", ondelete="SET NULL"), nullable=False)

    status = Column(String(32), default="active")  # active, cancelled, expired
    started_at = Column(DateTime, default=datetime.utcnow)
    ended_at = Column(DateTime, nullable=True)

    # İlişkiler
    user = relationship('User', backref='memberships')
    plan = relationship("Plan", back_populates="memberships")
