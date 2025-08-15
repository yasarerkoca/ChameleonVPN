# ~/ChameleonVPN/backend/app/crud/security/failed_login_attempt_crud.py

from sqlalchemy.orm import Session
from app.models.security.failed_login_attempt import FailedLoginAttempt
from datetime import datetime, timedelta

def log_failed_attempt(db: Session, ip: str, email: str = None):
    fail = FailedLoginAttempt(ip_address=ip, email=email)
    db.add(fail)
    db.commit()

def count_recent_failed_attempts(db: Session, ip: str, window_minutes: int = 15):
    window_start = datetime.utcnow() - timedelta(minutes=window_minutes)
    return db.query(FailedLoginAttempt).filter(
        FailedLoginAttempt.ip_address == ip,
        FailedLoginAttempt.attempt_time >= window_start
    ).count()

def clear_failed_attempts(db: Session, ip: str):
    db.query(FailedLoginAttempt).filter(
        FailedLoginAttempt.ip_address == ip
    ).delete()
    db.commit()

def clear_old_attempts(db: Session, days: int = 7):
    threshold = datetime.utcnow() - timedelta(days=days)
    db.query(FailedLoginAttempt).filter(
        FailedLoginAttempt.attempt_time < threshold
    ).delete()
    db.commit()
