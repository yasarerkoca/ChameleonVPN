from fastapi import APIRouter, Request, HTTPException, status
import os
import json
import hmac
import hashlib
import base64

router = APIRouter(
    prefix="/payment/webhook",
    tags=["payment-webhook"]
)

@router.post("/stripe", summary="Stripe webhook endpoint'i")
async def stripe_webhook(request: Request):
    """
    Stripe'dan gelen webhook'ları işler.
    """
    payload = await request.body()

    sig_header = request.headers.get("Stripe-Signature")
    secret = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    try:
        import stripe

        event = stripe.Webhook.construct_event(payload, sig_header, secret)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

    event_type = event.get("type")
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        _ = session.get("id")  # işlem placeholder
    return {"status": "received"}

@router.post("/iyzico", summary="iyzico webhook endpoint'i")
async def iyzico_webhook(request: Request):
    """
    iyzico'dan gelen webhook'ları işler.
    """
    payload = await request.body()

    signature = request.headers.get("x-iyz-signature", "")
    secret = os.getenv("IYZICO_SECRET_KEY", "")
    computed_sig = base64.b64encode(
        hmac.new(secret.encode(), payload, hashlib.sha1).digest()
    ).decode()
    if not hmac.compare_digest(computed_sig, signature):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature"
        )

    event = json.loads(payload)
    event_type = event.get("iyz_event_type") or event.get("eventType")
    if event_type == "payment.succeeded":
        payment_id = event.get("paymentId")
        _ = payment_id  # işlem placeholder

    return {"status": "received"}
