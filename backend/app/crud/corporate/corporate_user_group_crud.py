from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.corporate.corporate_user_group import CorporateUserGroup


def create_group(db: Session, name: str, description: Optional[str] = None) -> CorporateUserGroup:
    group = CorporateUserGroup(name=name, description=description)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


def get_group_by_id(db: Session, group_id: int) -> Optional[CorporateUserGroup]:
    return db.query(CorporateUserGroup).filter(CorporateUserGroup.id == group_id).first()


def get_all_groups(db: Session) -> List[CorporateUserGroup]:
    return db.query(CorporateUserGroup).all()
