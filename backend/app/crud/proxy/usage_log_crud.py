from sqlalchemy.orm import Session
from app.models.proxy.proxy_usage_log import ProxyUsageLog
from app.schemas.proxy.proxy_usage_log import ProxyUsageLogCreate


def add_proxy_usage_log(db: Session, log: ProxyUsageLogCreate) -> ProxyUsageLog:
    db_log = ProxyUsageLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


def get_user_usage_logs(db: Session, user_id: int):
    return db.query(ProxyUsageLog).filter(ProxyUsageLog.user_id == user_id).all()


def get_proxy_usage_logs(db: Session, proxy_id: int):
    return db.query(ProxyUsageLog).filter(ProxyUsageLog.proxy_id == proxy_id).all()
