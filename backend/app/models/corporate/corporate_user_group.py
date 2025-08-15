# ~/ChameleonVPN/backend/app/models/corporate/corporate_user_group.py

from sqlalchemy import Column, Integer, String, Boolean, Index
from sqlalchemy.orm import relationship

from app.config.database import Base


class CorporateUserGroup(Base):
    """
    Kurumsal kullanıcı grupları (örn. Acme Corp Adminleri, Teknik Grup, vs.)
    """
    __tablename__ = "corporate_user_groups"
    __table_args__ = (
        Index("ix_corporate_group_name", "name"),
        {"extend_existing": True},
    )

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)   # Grup adı
    max_proxies = Column(Integer, default=5)                  # Grup için maksimum proxy
    is_active = Column(Boolean, default=True)                 # Grup aktif mi?

    # user.py içinde: corporate_group = relationship("CorporateUserGroup", back_populates="users", foreign_keys=[corporate_group_id])
    users = relationship(
        "User",
        back_populates="corporate_group",
        foreign_keys="User.corporate_group_id",
    )

    def __repr__(self) -> str:
        return f"<CorporateUserGroup id={self.id} name='{self.name}' active={self.is_active}>"
