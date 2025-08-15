from sqlalchemy.orm import Session
from typing import List
from app.models.corporate.corporate_user_rights_history import CorporateUserRightsHistory


def log_rights_change(
    db: Session,
    user_id: int,
    previous_rights: str,
    new_rights: str,
    changed_by: int,
) -> CorporateUserRightsHistory:
    log = CorporateUserRightsHistory(
        user_id=user_id,
        previous_rights=previous_rights,
        new_rights=new_rights,
        changed_by=changed_by,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log


def get_user_rights_history(db: Session, user_id: int) -> List[CorporateUserRightsHistory]:
    return db.query(CorporateUserRightsHistory).filter(CorporateUserRightsHistory.user_id == user_id).all()
