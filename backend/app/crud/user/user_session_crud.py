from sqlalchemy.orm import Session
from app.models.user.user_session import UserSession
from app.schemas.user.user_meta import UserSessionCreate
from typing import List


def create_user_session(db: Session, session_data: UserSessionCreate) -> UserSession:
    session = UserSession(**session_data.dict())
    db.add(session)
    db.commit()
    db.refresh(session)
    return session


def get_sessions_by_user(db: Session, user_id: int) -> List[UserSession]:
    return db.query(UserSession).filter(UserSession.user_id == user_id).order_by(
        UserSession.login_time.desc()
    ).all()


def end_user_session(db: Session, session_id: int) -> bool:
    session = db.query(UserSession).filter(UserSession.id == session_id).first()
    if not session:
        return False
    session.logout_time = session.logout_time or session.login_time  # logout_time ayarla
    db.commit()
    return True
