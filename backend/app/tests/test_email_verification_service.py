import os
import sys
from pathlib import Path
import pytest

# allow import app modules
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.services.email_verification_service import send_reset_email


@pytest.mark.asyncio
async def test_send_reset_email_uses_env(monkeypatch):
    captured = {}

    async def fake_send_email_async(to_email, subject, body, html_body=None):
        captured["to"] = to_email
        captured["subject"] = subject
        captured["body"] = body

    monkeypatch.setattr(
        "app.services.email_verification_service.send_email_async", fake_send_email_async
    )

    os.environ["PASSWORD_RESET_URL"] = "https://example.com/reset"
    await send_reset_email("user@example.com", "abc123")
    assert (
        "https://example.com/reset?email=user@example.com&token=abc123" in captured["body"]
    )
    del os.environ["PASSWORD_RESET_URL"]
