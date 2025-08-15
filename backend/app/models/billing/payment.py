# ~/ChameleonVPN/backend/app/models/billing/payment.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    plan_id = Column(Integer, ForeignKey("plans.id", ondelete="SET NULL"), nullable=False)

    amount = Column(Integer, nullable=False)
    status = Column(String(32), default="pending")  # pending, completed, failed, refunded
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', backref='payments')
    plan = relationship("Plan", back_populates="payments")
