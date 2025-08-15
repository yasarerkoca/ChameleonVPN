# app.services.email_2fa_service - 2FA kod gönderimi servisi

from app.utils.email.email_core import send_email_async
import logging

logger = logging.getLogger(__name__)


async def send_two_factor_code_email(to_email: str, code: str) -> None:
    """
    Belirtilen kullanıcıya 2FA doğrulama kodunu e-posta ile gönderir.

    Args:
        to_email (str): Kullanıcının e-posta adresi
        code (str): Doğrulama kodu
    """
    subject = "ChameleonVPN - İki Faktörlü Doğrulama Kodu"
    body = (
        f"Merhaba,\n\n"
        f"ChameleonVPN hesabınız için iki faktörlü doğrulama kodunuz:\n\n"
        f"{code}\n\n"
        f"Lütfen bu kodu kimseyle paylaşmayın.\n"
        f"İyi günler dileriz."
    )

    try:
        await send_email_async(to_email, subject, body)
        logger.info(f"2FA kodu e-postayla gönderildi: {to_email}")
    except Exception as e:
        logger.error(f"2FA kodu gönderimi başarısız: {to_email} - {str(e)}")
        raise
