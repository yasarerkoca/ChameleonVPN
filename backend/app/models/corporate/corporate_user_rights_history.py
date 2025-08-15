# ~/ChameleonVPN/backend/app/models/corporate/corporate_user_rights_history.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.config.database import Base


class CorporateUserRightsHistory(Base):
    """
    Kurumsal kullanıcıların yetki/geçmiş değişim kayıtları.
    """
    __tablename__ = "corporate_user_rights_history"
    __table_args__ = (
        Index("ix_corporate_rights_user_id", "user_id"),
        Index("ix_corporate_rights_changed_by", "changed_by_admin_id"),
        {'extend_existing': True},
    )

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    changed_by_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    field_changed = Column(String(64), nullable=False)      # Örn: 'role', 'group_id'
    old_value = Column(String(128), nullable=True)
    new_value = Column(String(128), nullable=True)
    changed_at = Column(DateTime, default=datetime.utcnow)
    note = Column(String(256), nullable=True)

    # Ana ilişkiler
    user = relationship('User', foreign_keys=[user_id], backref='corporate_rights_changes')
    changed_by_admin = relationship('User', foreign_keys=[changed_by_admin_id], backref='corporate_rights_changes')
