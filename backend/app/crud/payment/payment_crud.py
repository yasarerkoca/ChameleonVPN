from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.billing.payment import Payment
from app.models.proxy.user_proxy_assignment import UserProxyAssignment
from app.models.proxy.proxy_ip import ProxyIP
from app.schemas.payment.payment_base import PaymentCreate


def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    """
    Yeni ödeme kaydı oluşturur. Ödeme tipi proxy ise otomatik atama yapar.
    """
    db_payment = Payment(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)

    # Otomatik proxy veya kota işlemleri
    if payment.type == "proxy":
        assign_proxy_after_payment(db, payment.user_id)
    elif payment.type == "ek_kota":
        increase_existing_proxy_quota(db, payment.user_id)

    return db_payment


def assign_proxy_after_payment(db: Session, user_id: int):
    """
    Ödeme sonrası aktif bir proxy varsa kullanıcıya atar.
    """
    proxy = db.query(ProxyIP).filter(ProxyIP.is_active == True).first()
    if not proxy:
        raise HTTPException(status_code=404, detail="No available proxy")

    assignment = UserProxyAssignment(
        user_id=user_id,
        proxy_id=proxy.id,
        assigned_quota_mb=1024,
        is_active=True
    )
    db.add(assignment)
    proxy.is_active = False
    db.commit()


def increase_existing_proxy_quota(db: Session, user_id: int):
    """
    Kullanıcının son proxy atamasına kota ekler.
    """
    assignment = db.query(UserProxyAssignment).filter(
        UserProxyAssignment.user_id == user_id,
        UserProxyAssignment.is_active == True
    ).order_by(UserProxyAssignment.created_at.desc()).first()

    if assignment:
        assignment.assigned_quota_mb += 1024
        db.commit()


def get_all_payments(db: Session):
    return db.query(Payment).all()


def get_user_payments(db: Session, user_id: int):
    return db.query(Payment).filter(Payment.user_id == user_id).all()


def get_payment_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()
