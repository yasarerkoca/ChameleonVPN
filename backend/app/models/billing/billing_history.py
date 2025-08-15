# ~/ChameleonVPN/backend/app/models/billing/billing_history.py

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base

class BillingHistory(Base):
    __tablename__ = "billing_history"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)  # ForeignKey eklendi

    transaction_id = Column(String(128), nullable=False)
    amount = Column(Float, nullable=False)
    transaction_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(64), default="pending")

    user = relationship("User", back_populates="billing_histories")
