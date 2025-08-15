# ~/ChameleonVPN/backend/app/models/user/deleted_user.py

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.config.database import Base

class DeletedUser(Base):
    __tablename__ = "deleted_users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(256), nullable=False)
    deleted_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<DeletedUser email={self.email}>"
