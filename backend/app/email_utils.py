
import aiosmtplib
from email.message import EmailMessage
from app.config import SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS
async def send_email_async(to, subject, body):
    msg = EmailMessage()
    msg["From"] = SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)
    await aiosmtplib.send(
        msg, hostname=SMTP_SERVER, port=SMTP_PORT, username=SMTP_USER, password=SMTP_PASS, start_tls=True
    )
    