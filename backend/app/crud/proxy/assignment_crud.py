from sqlalchemy.orm import Session
from app.models.proxy.user_proxy_assignment import UserProxyAssignment
from app.schemas.proxy.user_proxy_assignment import UserProxyAssignmentCreate


def assign_proxy_to_user(db: Session, assignment: UserProxyAssignmentCreate) -> UserProxyAssignment:
    db_assignment = UserProxyAssignment(**assignment.dict())
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment


def get_user_assignments(db: Session, user_id: int):
    return db.query(UserProxyAssignment).filter(UserProxyAssignment.user_id == user_id).all()


def get_proxy_assignments(db: Session, proxy_id: int):
    return db.query(UserProxyAssignment).filter(UserProxyAssignment.proxy_id == proxy_id).all()


def get_assignment_by_id(db: Session, assignment_id: int):
    return db.query(UserProxyAssignment).filter(UserProxyAssignment.id == assignment_id).first()


def delete_assignment(db: Session, assignment_id: int):
    assignment = db.query(UserProxyAssignment).filter(UserProxyAssignment.id == assignment_id).first()
    if assignment:
        db.delete(assignment)
        db.commit()
    return assignment


def update_assignment(db: Session, assignment_id: int, data: UserProxyAssignmentCreate):
    assignment = db.query(UserProxyAssignment).filter(UserProxyAssignment.id == assignment_id).first()
    if not assignment:
        return None
    for key, value in data.dict().items():
        setattr(assignment, key, value)
    db.commit()
    db.refresh(assignment)
    return assignment
