from sqlalchemy.orm import Session
from app.models.proxy.proxy_ip import ProxyIP
from app.schemas.proxy.proxy_ip import ProxyIPCreate


def create_proxy_ip(db: Session, proxy: ProxyIPCreate) -> ProxyIP:
    db_proxy = ProxyIP(**proxy.dict())
    db.add(db_proxy)
    db.commit()
    db.refresh(db_proxy)
    return db_proxy


def get_all_proxy_ips(db: Session):
    return db.query(ProxyIP).all()


def get_proxy_ip(db: Session, proxy_id: int):
    return db.query(ProxyIP).filter(ProxyIP.id == proxy_id).first()


def update_proxy_ip(db: Session, proxy_id: int, data: ProxyIPCreate):
    proxy = db.query(ProxyIP).filter(ProxyIP.id == proxy_id).first()
    if not proxy:
        return None
    for key, value in data.dict().items():
        setattr(proxy, key, value)
    db.commit()
    db.refresh(proxy)
    return proxy


def delete_proxy_ip(db: Session, proxy_id: int):
    proxy = db.query(ProxyIP).filter(ProxyIP.id == proxy_id).first()
    if proxy:
        db.delete(proxy)
        db.commit()
    return proxy
