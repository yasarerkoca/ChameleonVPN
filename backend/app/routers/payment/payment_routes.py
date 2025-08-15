from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_admin  # admin koruması için ekle
from app.schemas.payment.payment_base import PaymentCreate, PaymentOut
from app.schemas.payment.plan_base import PlanCreate, PlanOut
from app.crud.payment.payment_crud import (
    create_payment, get_all_payments, get_user_payments, get_payment_by_id
)
from app.crud.payment.plan_crud import (
    create_plan, get_all_plans, get_plan_by_id
)

router = APIRouter(
    prefix="/admin/payment",
    tags=["admin-payment"]
)

# --------------------
# ÖDEME ENDPOINTLERİ
# --------------------

@router.post("/", response_model=PaymentOut, summary="Yeni ödeme kaydı oluştur")
def add_payment(
    payment: PaymentCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return create_payment(db, payment)

@router.get("/", response_model=List[PaymentOut], summary="Tüm ödemeleri listele")
def list_payments(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return get_all_payments(db)

@router.get("/user/{user_id}", response_model=List[PaymentOut], summary="Belirli kullanıcının ödemelerini listele")
def user_payments(
    user_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return get_user_payments(db, user_id)

@router.get("/{payment_id}", response_model=PaymentOut, summary="Ödeme kaydını getir")
def get_payment(
    payment_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

# --------------------
# PLAN ENDPOINTLERİ
# --------------------

@router.post("/plan", response_model=PlanOut, summary="Yeni plan oluştur")
def add_plan(
    plan: PlanCreate,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return create_plan(db, plan)

@router.get("/plan", response_model=List[PlanOut], summary="Tüm planları listele")
def list_plans(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    return get_all_plans(db)

@router.get("/plan/{plan_id}", response_model=PlanOut, summary="Plan detaylarını getir")
def get_plan(
    plan_id: int,
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    plan = get_plan_by_id(db, plan_id)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan
