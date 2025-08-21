import os
import sys
from pathlib import Path
import pytest

# Ensure required settings exist before importing
os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("SECRET_KEY", "x" * 32)
os.environ.setdefault("SESSION_SECRET_KEY", "y" * 32)
os.environ.setdefault("PASSWORD_RESET_URL", "https://example.com/reset")
os.environ.setdefault("EMAIL_VERIFY_URL", "https://example.com/verify")

# allow import app modules
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.email_verification_service import send_reset_email
from app.config.base import settings

@pytest.mark.asyncio
async def test_send_reset_email_uses_settings(monkeypatch):
    captured = {}

    async def fake_send_email_async(to_email, subject, body, html_body=None):
        captured["to"] = to_email
        captured["subject"] = subject
        captured["body"] = body

    monkeypatch.setattr(
        "app.services.email_verification_service.send_email_async", fake_send_email_async
    )
    monkeypatch.setattr(settings, "PASSWORD_RESET_URL", "https://example.com/reset")

    await send_reset_email("user@example.com", "abc123")
    assert (
        "https://example.com/reset?email=user@example.com&token=abc123" in captured["body"]
    )
