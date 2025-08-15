from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from app.config.database import Base

class UserBillingHistory(Base):
    __tablename__ = "user_billing_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    action = Column(String(64), nullable=False)  # 'payment', 'refund', 'upgrade', vs.
    amount = Column(Float, nullable=False)
    currency = Column(String(8), default="USD")
    created_at = Column(DateTime)
    notes = Column(String(256), nullable=True)
