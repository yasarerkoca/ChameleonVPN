# ~/ChameleonVPN/backend/app/models/corporate/corporate_user_rights_history.py

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.config.database import Base


class CorporateUserRightsHistory(Base):
    """
    Kurumsal kullanıcıların yetki/değişiklik geçmişi kayıtları.
    """
    __tablename__ = "corporate_user_rights_history"
    __table_args__ = (
        Index("ix_corporate_rights_user_id", "user_id"),
        Index("ix_corporate_rights_changed_by", "changed_by_admin_id"),
        Index("ix_corporate_rights_changed_at", "changed_at"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, index=True)

    # Değişikliği yaşayan kullanıcı
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # Değişikliği yapan admin (nullable olabilir)
    changed_by_admin_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    field_changed = Column(String(64), nullable=False)  # Örn: 'role', 'group_id'
    old_value = Column(String(128), nullable=True)
    new_value = Column(String(128), nullable=True)

    # DB tarafı zaman damgası tercih edildi
    changed_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    note = Column(String(256), nullable=True)

    # İlişkiler — backref yerine back_populates (çakışmayı önler)
    user = relationship(
        "User",
        foreign_keys=[user_id],
        back_populates="corporate_rights_history",
        passive_deletes=True,
    )

    changed_by_admin = relationship(
        "User",
        foreign_keys=[changed_by_admin_id],
        back_populates="admin_rights_changes",
        passive_deletes=True,
    )

    def __repr__(self) -> str:
        return (
            f"<CorporateUserRightsHistory id={self.id} "
            f"user_id={self.user_id} admin_id={self.changed_by_admin_id} "
            f"field={self.field_changed} old={self.old_value} new={self.new_value}>"
        )
