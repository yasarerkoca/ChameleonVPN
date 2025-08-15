from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.billing.plan import Plan
from app.schemas.payment.plan_base import PlanCreate


def create_plan(db: Session, plan_data: PlanCreate) -> Plan:
    plan = Plan(**plan_data.dict())
    db.add(plan)
    db.commit()
    db.refresh(plan)
    return plan


def get_all_plans(db: Session) -> List[Plan]:
    return db.query(Plan).filter(Plan.is_active == True).all()


def get_plan_by_id(db: Session, plan_id: int) -> Optional[Plan]:
    return db.query(Plan).filter(Plan.id == plan_id).first()


def deactivate_plan(db: Session, plan_id: int) -> bool:
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        plan.is_active = False
        db.commit()
        return True
    return False
