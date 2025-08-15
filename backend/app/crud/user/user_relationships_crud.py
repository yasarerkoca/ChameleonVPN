from sqlalchemy.orm import Session
from app.models.user.user_relationships import UserRelationship
from app.schemas.user.user_meta import UserRelationshipCreate
from typing import List


def create_relationship(db: Session, relationship_data: UserRelationshipCreate) -> UserRelationship:
    relation = UserRelationship(**relationship_data.dict())
    db.add(relation)
    db.commit()
    db.refresh(relation)
    return relation


def get_relationships_of_user(db: Session, user_id: int) -> List[UserRelationship]:
    return db.query(UserRelationship).filter(
        (UserRelationship.user_id == user_id) | (UserRelationship.related_user_id == user_id)
    ).all()


def delete_relationship(db: Session, relationship_id: int) -> bool:
    rel = db.query(UserRelationship).filter(UserRelationship.id == relationship_id).first()
    if not rel:
        return False
    db.delete(rel)
    db.commit()
    return True
