# ~/ChameleonVPN/backend/app/models/corporate/corporate_user_group.py

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.config.database import Base

class CorporateUserGroup(Base):
    """
    Kurumsal kullanıcı grupları (örn. Acme Corp Adminleri, Teknik Grup, vs.)
    """
    __tablename__ = "corporate_user_groups"
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)   # Grup adı
    max_proxies = Column(Integer, default=5)                  # Grup için maksimum proxy
    is_active = Column(Boolean, default=True)                 # Grup aktif mi?

    # İlişki (user.py'da karşılığı: corporate_group = relationship(...))
    users = relationship('User', backref='corporate_group')
