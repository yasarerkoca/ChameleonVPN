import stripe
import os

# .env veya config dosyandan anahtarları çek
STRIPE_API_KEY = os.getenv("STRIPE_API_KEY", "sk_test_xxx")  # Gerçek anahtarını ekle

stripe.api_key = STRIPE_API_KEY

def create_stripe_payment_intent(amount: float, currency: str = "usd") -> dict:
    """
    Stripe PaymentIntent oluşturur ve client_secret döner.
    """
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(amount * 100),  # Stripe kuruş (cent) olarak ister
            currency=currency,
            payment_method_types=["card"],
        )
        return {
            "client_secret": intent.client_secret,
            "payment_intent_id": intent.id
        }
    except stripe.error.StripeError as e:
        raise Exception(f"Stripe hata: {str(e)}")

def verify_stripe_event(payload: bytes, sig_header: str, webhook_secret: str):
    """
    Stripe webhook doğrulaması (güvenlik için).
    """
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
        return event
    except stripe.error.SignatureVerificationError:
        raise Exception("Webhook doğrulama başarısız.")

# Ek: İhtiyaca göre müşteri, subscription vs. fonksiyonları eklenebilir
