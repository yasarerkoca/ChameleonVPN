# app.utils.email.email_core - SMTP tabanlı async e-posta gönderimi

import os
import aiosmtplib
from email.message import EmailMessage
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# SMTP ayarlarını ortam değişkenlerinden al
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)


async def send_email_async(
    to_email: str,
    subject: str,
    body: str,
    html_body: Optional[str] = None,
) -> None:
    """
    Asenkron şekilde SMTP ile e-posta gönderir.

    Args:
        to_email (str): Alıcı e-posta adresi
        subject (str): E-posta başlığı
        body (str): Düz metin e-posta içeriği
        html_body (Optional[str]): HTML formatında içerik
    """
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASS]):
        logger.error("SMTP yapılandırması eksik. .env dosyasını kontrol edin.")
        return

    msg = EmailMessage()
    msg["From"] = SMTP_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype="html")

    try:
        await aiosmtplib.send(
            msg,
            hostname=SMTP_HOST,
            port=SMTP_PORT,
            username=SMTP_USER,
            password=SMTP_PASS,
            start_tls=True,
        )
        logger.info(f"E-posta gönderildi: {to_email} - {subject}")
    except Exception as e:
        logger.error(f"E-posta gönderimi başarısız: {to_email} - {str(e)}")
        raise
