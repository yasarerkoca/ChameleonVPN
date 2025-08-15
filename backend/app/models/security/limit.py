from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserLimit(Base):
    __tablename__ = "user_limits"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    limit_type = Column(String(64), nullable=False)  # Örn: proxy_quota, vpn_bandwidth
    value = Column(Integer, default=0)

    # İlişki
    user = relationship('User', back_populates='limits')

    def __repr__(self):
        return f"<UserLimit user_id={self.user_id}, type={self.limit_type}, value={self.value}>"
