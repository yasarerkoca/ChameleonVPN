from fastapi import APIRouter, HTTPException, Body
from typing import Optional
import os
import uuid
import json

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
    try:
        import stripe

        stripe.api_key = os.getenv("STRIPE_API_KEY", "")
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": currency,
                        "unit_amount": int(amount * 100),
                        "product_data": {"name": "ChameleonVPN Subscription"},
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            customer_email=customer_email,
            success_url=os.getenv("STRIPE_SUCCESS_URL", "https://example.com/success"),
            cancel_url=os.getenv("STRIPE_CANCEL_URL", "https://example.com/cancel"),
        )
        return {"status": "ok", "session_id": session.get("id")}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

# Örnek: iyzico ödeme başlatma endpoint'i
@router.post("/iyzico/initialize", summary="iyzico ödeme başlat")
def initialize_iyzico_payment(
    price: float = Body(..., embed=True),
    currency: str = Body("TRY", embed=True),
    customer_email: Optional[str] = Body(None, embed=True),
):
    """
    iyzico ile yeni bir ödeme başlatır.
    """
    try:
        import iyzipay

        options = iyzipay.Options()
        options.api_key = os.getenv("IYZICO_API_KEY", "")
        options.secret_key = os.getenv("IYZICO_SECRET_KEY", "")
        options.base_url = os.getenv(
            "IYZICO_BASE_URL", "https://sandbox-api.iyzipay.com"
        )

        request_payload = {
            "locale": "tr",
            "conversationId": str(uuid.uuid4()),
            "price": price,
            "paidPrice": price,
            "currency": currency,
            "basketId": "B67832",
            "paymentGroup": "PRODUCT",
            "callbackUrl": os.getenv(
                "IYZICO_CALLBACK_URL", "https://example.com/iyzico/callback"
            ),
            "buyer": {
                "id": "BY789",
                "name": "John",
                "surname": "Doe",
                "email": customer_email,
                "identityNumber": "74300864791",
                "registrationAddress": "Istanbul",
                "ip": "85.34.78.112",
                "city": "Istanbul",
                "country": "Turkey",
            },
            "billingAddress": {
                "contactName": "John Doe",
                "city": "Istanbul",
                "country": "Turkey",
                "address": "Istanbul",
            },
            "shippingAddress": {
                "contactName": "John Doe",
                "city": "Istanbul",
                "country": "Turkey",
                "address": "Istanbul",
            },
            "basketItems": [
                {
                    "id": "BI101",
                    "name": "ChameleonVPN Subscription",
                    "category1": "VPN",
                    "itemType": "VIRTUAL",
                    "price": price,
                }
            ],
        }

        checkout_form = iyzipay.CheckoutFormInitialize().create(
            request_payload, options
        )
        result = json.loads(checkout_form.read().decode("utf-8"))
        token = result.get("token")
        if not token:
            raise HTTPException(status_code=400, detail=result)
        return {"status": "ok", "payment_id": token}
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

