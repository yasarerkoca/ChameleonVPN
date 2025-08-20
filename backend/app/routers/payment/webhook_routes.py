from fastapi import APIRouter, Request, HTTPException, status
import os
import json
import hmac
import hashlib
import base64
import logging
from typing import Optional

from sqlalchemy.orm import Session

from app.config.database import SessionLocal
from app.models.billing.payment import Payment
from app.models.billing.billing_history import BillingHistory

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/payment/webhook",
    tags=["payment-webhook"]
)

def _verify_stripe_signature(payload: bytes, sig_header: str):
    secret = os.getenv("STRIPE_WEBHOOK_SECRET")
    if not secret:
        logger.error("Stripe webhook secret is not configured")
        raise HTTPException(status_code=500, detail="Stripe secret not configured")
    try:
        import stripe
    except ImportError as exc:
        logger.exception("Stripe SDK not installed")
        raise HTTPException(status_code=500, detail="Stripe SDK not installed") from exc

    try:
        return stripe.Webhook.construct_event(payload, sig_header, secret)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")

def _handle_stripe_event(event: dict, db: Optional[Session] = None):
    event_type = event.get("type")
    if event_type == "checkout.session.completed":
        session = event["data"]["object"]
        session_id = session.get("id")
        logger.info("Stripe session completed: %s", session_id)

        payment_id = session.get("metadata", {}).get("payment_id")
        if not payment_id:
            return

        local_db = db or SessionLocal()
        try:
            payment = (
                local_db.query(Payment)
                .filter(Payment.id == int(payment_id))
                .first()
            )
            if payment:
                payment.status = "completed"
                billing = BillingHistory(
                    user_id=payment.user_id,
                    transaction_id=session_id,
                    amount=payment.amount,
                    status="completed",
                )
                local_db.add(billing)
                local_db.commit()
            else:
                logger.warning("Payment not found for id %s", payment_id)
        finally:
            if db is None:
                local_db.close()

def _verify_iyzico_signature(payload: bytes, signature: str):
    secret = os.getenv("IYZICO_SECRET_KEY")
    if not secret:
        logger.error("IYZICO secret key not configured")
        raise HTTPException(status_code=500, detail="IYZICO secret not configured")
    computed_sig = base64.b64encode(
        hmac.new(secret.encode(), payload, hashlib.sha1).digest()
    ).decode()
    if not hmac.compare_digest(computed_sig, signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid signature")
    return json.loads(payload)

def _handle_iyzico_event(event: dict, db: Optional[Session] = None):
    event_type = event.get("iyz_event_type") or event.get("eventType")
    if event_type == "payment.succeeded":
        payment_id = event.get("paymentId")
        logger.info("iyzico payment succeeded: %s", payment_id)
        if not payment_id:
            return

        local_db = db or SessionLocal()
        try:
            payment = (
                local_db.query(Payment)
                .filter(Payment.id == int(payment_id))
                .first()
            )
            if payment:
                payment.status = "completed"
                billing = BillingHistory(
                    user_id=payment.user_id,
                    transaction_id=str(payment_id),
                    amount=payment.amount,
                    status="completed",
                )
                local_db.add(billing)
                local_db.commit()
            else:
                logger.warning("Payment not found for id %s", payment_id)
        finally:
            if db is None:
                local_db.close()
@router.post("/stripe", summary="Stripe webhook endpoint'i")
async def stripe_webhook(request: Request):
    """Stripe'dan gelen webhook'ları işler."""
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature", "")
    event = _verify_stripe_signature(payload, sig_header)
    _handle_stripe_event(event)
    return {"status": "received"}

@router.post("/iyzico", summary="iyzico webhook endpoint'i")
async def iyzico_webhook(request: Request):
    """iyzico'dan gelen webhook'ları işler."""
    payload = await request.body()
    signature = request.headers.get("x-iyz-signature", "")
    event = _verify_iyzico_signature(payload, signature)
    _handle_iyzico_event(event)
    return {"status": "received"}
