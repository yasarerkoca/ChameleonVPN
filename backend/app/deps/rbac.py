# ~/ChameleonVPN/backend/app/deps/rbac.py

"""RBAC related dependencies and helpers."""

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.utils.auth.auth_utils import get_current_user
from app.models.user.user import User
from app.models.role import Role


def require_role(*roles: str):
    """Return a dependency ensuring the current user has one of the roles."""

    def _checker(current_user: User = Depends(get_current_user)) -> User:
        user_roles = {r.name for r in getattr(current_user, "roles", [])}
        if getattr(current_user, "is_admin", False):
            user_roles.add("admin")
        if not user_roles.intersection(set(roles)):
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return current_user

    return _checker


def seed_default_roles(db: Session) -> None:
    """Create default roles if they do not exist."""

    default_roles = {"admin", "user"}
    existing = {r.name for r in db.query(Role).filter(Role.name.in_(default_roles)).all()}
    for role_name in default_roles - existing:
        db.add(Role(name=role_name))
    db.commit()
