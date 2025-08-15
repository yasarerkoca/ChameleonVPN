# ~/ChameleonVPN/backend/app/models/user/user_external_auth.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.config.database import Base

class UserExternalAuth(Base):
    __tablename__ = "user_external_auths"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    provider = Column(String(64), nullable=False)              # Örn: google, github, facebook
    provider_user_id = Column(String(128), nullable=False)     # Sağlayıcıya özel kullanıcı ID'si

    user = relationship('User', backref='external_auths')

    def __repr__(self):
        return f"<UserExternalAuth user_id={self.user_id}, provider={self.provider}>"
