# ~/ChameleonVPN/backend/app/crud/payment/membership_crud.py

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from fastapi import HTTPException
from typing import List, Optional

from app.models.user.user import User
from app.models.billing.plan import Plan
from app.models.billing.membership import Membership


def get_all_plans(db: Session) -> List[Plan]:
    """
    Tüm aktif abonelik planlarını getirir.
    """
    return db.query(Plan).filter(Plan.is_active == True).all()


def get_plan_by_id(db: Session, plan_id: int) -> Optional[Plan]:
    """
    Belirli bir planı ID ile getirir.
    """
    return db.query(Plan).filter(Plan.id == plan_id, Plan.is_active == True).first()


def create_membership(db: Session, user: User, plan: Plan) -> Membership:
    """
    Yeni kullanıcı üyeliği oluşturur.
    """
    now = datetime.utcnow()
    end_date = now + timedelta(days=plan.duration_days)

    new_membership = Membership(
        user_id=user.id,
        plan_id=plan.id,
        start_date=now,
        end_date=end_date,
        is_active=True,
        quota_total=plan.quota,
        quota_used=0,
        proxy_quota_total=plan.proxy_quota,
        proxy_quota_used=0,
        price=plan.price
    )

    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership


def get_active_membership(db: Session, user_id: int) -> Membership:
    """
    Kullanıcının aktif üyeliğini getirir.
    """
    return db.query(Membership).filter(
        Membership.user_id == user_id,
        Membership.is_active == True,
        Membership.end_date > datetime.utcnow()
    ).first()


def get_quota_status(db: Session, user_id: int) -> dict:
    """
    Kullanıcının VPN/proxy kota durumunu getirir.
    """
    membership = get_active_membership(db, user_id)
    if not membership:
        raise HTTPException(status_code=404, detail="No active membership")
    return {
        "quota_total": membership.quota_total,
        "quota_used": membership.quota_used,
        "proxy_quota_total": membership.proxy_quota_total,
        "proxy_quota_used": membership.proxy_quota_used,
    }


def upgrade_membership(db: Session, user: User, new_plan_id: int) -> Membership:
    """
    Kullanıcının planını yükseltir.
    """
    plan = get_plan_by_id(db, new_plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    membership = get_active_membership(db, user.id)
    if not membership:
        raise HTTPException(status_code=400, detail="No active membership")

    membership.plan_id = plan.id
    membership.quota_total = plan.quota
    membership.proxy_quota_total = plan.proxy_quota
    membership.price = plan.price
    membership.end_date = datetime.utcnow() + timedelta(days=plan.duration_days)

    db.commit()
    db.refresh(membership)
    return membership


def cancel_membership(db: Session, user_id: int) -> None:
    """
    Kullanıcının mevcut üyeliğini iptal eder.
    """
    membership = get_active_membership(db, user_id)
    if not membership:
        raise HTTPException(status_code=400, detail="No active membership")
    membership.is_active = False
    db.commit()
