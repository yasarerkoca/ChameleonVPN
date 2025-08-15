from sqlalchemy.orm import Session
from app.models.proxy.proxy_request import ProxyRequest
from app.schemas.proxy.proxy_request import ProxyRequestCreate


def create_proxy_request(db: Session, request_data: ProxyRequestCreate) -> ProxyRequest:
    proxy_request = ProxyRequest(**request_data.dict())
    db.add(proxy_request)
    db.commit()
    db.refresh(proxy_request)
    return proxy_request


def get_pending_requests(db: Session):
    return db.query(ProxyRequest).filter(ProxyRequest.status == "pending").all()
