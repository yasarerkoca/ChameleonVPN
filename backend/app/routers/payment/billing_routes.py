from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user
from app.schemas.payment.user_billing_history import UserBillingHistoryOut
from app.schemas.payment.user_subscription_history import UserSubscriptionHistoryOut
from app.models.user.user import User
from app.crud.billing.billing import (  # GÜNCELLENDİ
    get_user_billing_history,
    get_user_subscription_history
)

router = APIRouter(
    prefix="/payment/billing",
    tags=["payment-billing"]
)

@router.get("/history", response_model=List[UserBillingHistoryOut], summary="Kullanıcının fatura geçmişini getir")
def billing_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Giriş yapan kullanıcının tüm ödeme/fatura kayıtlarını listeler.
    """
    return get_user_billing_history(db, current_user.id)

@router.get("/subscription-history", response_model=List[UserSubscriptionHistoryOut], summary="Kullanıcının abonelik geçmişini getir")
def subscription_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Giriş yapan kullanıcının tüm abonelik değişim geçmişini listeler.
    """
    return get_user_subscription_history(db, current_user.id)
