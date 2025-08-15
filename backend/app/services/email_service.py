# app.services.email_service - Genel e-posta gönderim servisi

from app.utils.email.email_core import send_email_async
import logging

logger = logging.getLogger(__name__)


async def send_general_email(to_email: str, subject: str, body: str) -> None:
    """
    Belirtilen e-posta adresine genel bir e-posta gönderir.

    Args:
        to_email (str): Alıcı e-posta adresi
        subject (str): E-posta başlığı
        body (str): E-posta gövdesi
    """
    try:
        await send_email_async(to_email, subject, body)
        logger.info(f"E-posta gönderildi: {to_email} - {subject}")
    except Exception as e:
        logger.error(f"E-posta gönderimi başarısız: {to_email} - {str(e)}")
        raise
