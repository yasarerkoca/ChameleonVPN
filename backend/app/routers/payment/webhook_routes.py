from fastapi import APIRouter, Request, HTTPException, status

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
    # TODO: Stripe imza doğrulama ve event ayrıştırma işlemleri buraya
    # event = stripe.Webhook.construct_event(...)
    # Event türüne göre ilgili işlemleri başlat
    # Örnek:
    # if event['type'] == 'checkout.session.completed': ...
    return {"status": "received"}

@router.post("/iyzico", summary="iyzico webhook endpoint'i")
async def iyzico_webhook(request: Request):
    """
    iyzico'dan gelen webhook'ları işler.
    """
    payload = await request.body()
    # TODO: iyzico ile imza ve event doğrulama işlemleri buraya
    return {"status": "received"}

