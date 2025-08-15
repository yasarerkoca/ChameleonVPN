# ~/ChameleonVPN/backend/app/models/user/user_relationships.py

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserRelationship(Base):
    __tablename__ = "user_relationships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    related_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    relationship_type = Column(String(64), nullable=False)  # friend, blocked, referral, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship('User', backref='relationships', foreign_keys=[user_id])
    related_user = relationship("User", foreign_keys=[related_user_id])

    def __repr__(self):
        return f"<UserRelationship user_id={self.user_id} related_user_id={self.related_user_id} type={self.relationship_type}>"
