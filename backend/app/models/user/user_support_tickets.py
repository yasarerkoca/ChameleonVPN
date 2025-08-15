# ~/ChameleonVPN/backend/app/models/user/user_support_tickets.py

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserSupportTicket(Base):
    __tablename__ = "user_support_tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    subject = Column(String(128), nullable=False)
    message = Column(Text, nullable=False)
    status = Column(String(32), default="open")  # open, pending, resolved, closed

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship('User', backref='support_tickets')

    def __repr__(self):
        return f"<UserSupportTicket id={self.id} user_id={self.user_id} status={self.status}>"
