# ~/ChameleonVPN/backend/app/models/billing/plan.py

from sqlalchemy import Column, Integer, String, Float, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base

class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500), nullable=True)
    price = Column(Float, nullable=False)
    duration_days = Column(Integer, default=30)  # Örn: 30 günlük plan
    is_active = Column(Boolean, default=True)  # aktif/pasif için bool daha doğru

    memberships = relationship("Membership", back_populates="plan", cascade="all, delete")
    payments = relationship("Payment", back_populates="plan", cascade="all, delete")

    def __repr__(self):
        return f"<Plan(name='{self.name}', price={self.price}, active={self.is_active})>"
