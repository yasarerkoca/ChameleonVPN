# app.services.email_verification_service - Doğrulama ve şifre sıfırlama e-posta servisi

from app.utils.email.email_core import send_email_async
import logging
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from app.config.base import settings

logger = logging.getLogger(__name__)

templates_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
env = Environment(
    loader=FileSystemLoader(templates_dir),
    autoescape=select_autoescape(["html", "xml"]),
)

async def send_verification_email(to_email: str, verify_url: str) -> None:
    """
    Hesap doğrulama bağlantısını içeren e-posta gönderir.

    Args:
        to_email (str): Kullanıcının e-posta adresi
        verify_url (str): Doğrulama linki
    """
    subject = "ChameleonVPN - Hesabınızı Doğrulayın"
    template = env.get_template("email/verify.html")
    html_body = template.render(verify_url=verify_url)
    body = (
        f"Merhaba,\n\n"
        f"Hesabınızı doğrulamak için aşağıdaki bağlantıya tıklayın:\n{verify_url}\n\n"
        f"Eğer bu isteği siz yapmadıysanız lütfen dikkate almayın."
    )

    try:
        await send_email_async(to_email, subject, body, html_body)
        logger.info(f"Doğrulama e-postası gönderildi: {to_email}")
    except Exception as e:
        logger.error(f"Doğrulama e-postası gönderimi başarısız: {to_email} - {str(e)}")
        raise


async def send_reset_email(to_email: str, token: str) -> None:
    """
    Şifre sıfırlama bağlantısını içeren e-posta gönderir.

    Args:
        to_email (str): Kullanıcının e-posta adresi
        token (str): Şifre sıfırlama için token
    """
    base_url = settings.PASSWORD_RESET_URL
    reset_link = f"{base_url}?email={to_email}&token={token}"
    subject = "ChameleonVPN - Şifre Sıfırlama"
    body = (
        f"Merhaba,\n\n"
        f"Şifrenizi sıfırlamak için aşağıdaki bağlantıya tıklayın:\n{reset_link}\n\n"
        f"Bu bağlantı yalnızca kısa bir süre geçerlidir."
    )

    try:
        await send_email_async(to_email, subject, body)
        logger.info(f"Şifre sıfırlama e-postası gönderildi: {to_email}")
    except Exception as e:
        logger.error(f"Şifre sıfırlama e-postası gönderimi başarısız: {to_email} - {str(e)}")
        raise
