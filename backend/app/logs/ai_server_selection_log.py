# ~/ChameleonVPN/backend/app/logs/ai_server_selection_log.py

from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class AIServerSelectionLog(Base):
    __tablename__ = "ai_server_selection_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_ip = Column(String(64), nullable=False)
    selected_server_id = Column(Integer, ForeignKey("vpn_servers.id", ondelete="SET NULL"))
    score = Column(Float, nullable=False)
    country = Column(String(8), nullable=True)
    reason = Column(String(256), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    vpn_server = relationship("VPNServer", backref="ai_selection_logs")

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return (
            f"<AIServerSelectionLog ip={self.user_ip} server={self.selected_server_id} "
            f"score={self.score}>"
        )
