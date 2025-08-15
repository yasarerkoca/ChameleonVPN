# ~/ChameleonVPN/backend/app/models/user/user_relationships.py

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserRelationship(Base):
    __tablename__ = "user_relationships"
    __table_args__ = (
        UniqueConstraint("user_id", "related_user_id", name="uq_user_rel_pair"),
        Index("ix_user_relationships_user_id", "user_id"),
        Index("ix_user_relationships_related_user_id", "related_user_id"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, index=True)

    # Her iki FK de users.id'ye gider (ambiguity buradan doğuyordu):
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    related_user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    relation_type = Column(String(32), nullable=False, default="follow")  # örnek: follow/block/mute
    status = Column(String(16), nullable=False, default="active")

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, nullable=True)

    # Netleştirilmiş ilişkiler (foreign_keys ile):
    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="relationships",
    )
    related_user = relationship(
        "User",
        foreign_keys=[related_user_id],
        back_populates="related_relationships",
    )

    def __repr__(self):
        return f"<UserRelationship {self.user_id}->{self.related_user_id} type={self.relation_type} status={self.status}>"
