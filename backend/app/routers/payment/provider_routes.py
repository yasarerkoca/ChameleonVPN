from fastapi import APIRouter, HTTPException, Body
from typing import Optional

router = APIRouter(
    prefix="/payment/provider",
    tags=["payment-provider"]
)

# Örnek: Stripe ödeme başlatma endpoint'i
@router.post("/stripe/create-session", summary="Stripe ödeme oturumu başlat")
def create_stripe_session(
    amount: float = Body(..., embed=True),
    currency: str = Body("usd", embed=True),
    customer_email: Optional[str] = Body(None, embed=True)
):
    """
    Stripe ile yeni bir ödeme oturumu başlatır.
    """
    # TODO: Stripe SDK entegrasyonu ve sessionId oluşturma kodu buraya eklenecek
    # stripe.checkout.Session.create(...)
    return {
        "status": "ok",
        "session_id": "dummy-session-id"
    }

# Örnek: iyzico ödeme başlatma endpoint'i
@router.post("/iyzico/initialize", summary="iyzico ödeme başlat")
def initialize_iyzico_payment(
    price: float = Body(..., embed=True),
    currency: str = Body("TRY", embed=True),
    customer_email: Optional[str] = Body(None, embed=True)
):
    """
    iyzico ile yeni bir ödeme başlatır.
    """
    # TODO: iyzico SDK ile ödeme başlatma kodu buraya eklenecek
    return {
        "status": "ok",
        "payment_id": "dummy-payment-id"
    }
