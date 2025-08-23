# ~/ChameleonVPN/backend/app/logs/ai_server_selection_log.py
"""AI server selection logging model."""

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class AIServerSelectionLog(Base):
    """Stores selections made by the AI server chooser."""

    __tablename__ = "ai_server_selection_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_ip = Column(String(64), nullable=False)
    selected_server_id = Column(
        Integer, ForeignKey("vpn_servers.id", ondelete="SET NULL"), nullable=True, index=True
    )
    score = Column(Float, nullable=True)
    country = Column(String(64), nullable=True)
    reason = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    selected_server = relationship("VPNServer", backref="ai_selection_logs")

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return (
            f"<AIServerSelectionLog user_ip={self.user_ip} server_id={self.selected_server_id} "
            f"score={self.score}>"
        )


__all__ = ["AIServerSelectionLog"]
