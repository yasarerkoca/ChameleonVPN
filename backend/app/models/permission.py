# ~/ChameleonVPN/backend/app/models/permission.py

"""Permission model for RBAC."""

from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship

from app.config.database import Base
from .role import role_permissions


# Association table between users and permissions
user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "permission_id",
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Permission(Base):
    """Represents a permission that can be attached to roles or users."""

    __tablename__ = "permissions"
    __table_args__ = {"extend_existing": True}

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    users = relationship(
        "User", secondary=user_permissions, back_populates="permissions"
    )
    roles = relationship(
        "Role", secondary=role_permissions, back_populates="permissions"
    )

    def __repr__(self) -> str:  # pragma: no cover - simple repr
        return f"<Permission id={self.id} name={self.name}>"
