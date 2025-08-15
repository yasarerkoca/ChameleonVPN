from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.proxy.proxy_ip import ProxyIP
from app.models.proxy.proxy_usage_log import ProxyUsageLog
from app.schemas.proxy.proxy_out import ProxyOut, ProxyPurchaseRequest, ProxyQuotaOut


def get_all_proxies(db: Session):
    return db.query(ProxyIP).all()


def get_proxy_logs_for_user(db: Session, user_id: int):
    return db.query(ProxyUsageLog).filter(ProxyUsageLog.user_id == user_id).all()


def get_user_proxies(db: Session, user_id: int):
    return db.query(ProxyIP).filter(ProxyIP.user_id == user_id).all()


def get_proxy_quota_status(db: Session, user_id: int) -> ProxyQuotaOut:
    used = db.query(ProxyIP).filter(ProxyIP.user_id == user_id).count()
    return ProxyQuotaOut(used=used, limit=5)  # Örnek limit değeri


def purchase_proxy(db: Session, user_id: int, proxy_id: int) -> ProxyOut:
    proxy = db.query(ProxyIP).filter(ProxyIP.id == proxy_id).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="Proxy not found")
    proxy.user_id = user_id
    db.commit()
    db.refresh(proxy)
    return proxy


def get_proxy_logs(db: Session, user_id: int):
    return db.query(ProxyUsageLog).filter(ProxyUsageLog.user_id == user_id).all()
