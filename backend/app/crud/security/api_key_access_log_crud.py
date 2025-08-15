from sqlalchemy.orm import Session
from app.models.security.api_key_access_log import APIKeyAccessLog


def log_api_key_access(db: Session, api_key_id: int, path: str, ip_address: str):
    log = APIKeyAccessLog(api_key_id=api_key_id, path=path, ip_address=ip_address)
    db.add(log)
    db.commit()
    db.refresh(log)
    return log
