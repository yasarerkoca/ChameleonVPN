# ~/ChameleonVPN/backend/app/logs/anomaly_fraud_record.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class AnomalyFraudRecord(Base):
    __tablename__ = "anomaly_fraud_records"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    ip_address = Column(String(64), nullable=True)
    reason = Column(String(256), nullable=False)
    detail = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="anomaly_records")

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return f"<AnomalyFraudRecord user_id={self.user_id} reason={self.reason}>"
