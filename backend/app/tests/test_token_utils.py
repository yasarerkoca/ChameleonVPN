import os
import sys
from pathlib import Path
from datetime import timedelta

# Ensure required settings exist before importing
os.environ.setdefault("DATABASE_URL", "sqlite:///test.db")
os.environ.setdefault("SECRET_KEY", "x"*32)
os.environ.setdefault("SESSION_SECRET_KEY", "y"*32)

# Allow `import app` from the backend package
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.utils.token.token_utils import create_access_token, decode_token


def test_create_and_decode_token_roundtrip():
    token = create_access_token({"sub": "user@example.com"}, expires_delta=timedelta(minutes=1))
    payload = decode_token(token)
    assert payload["sub"] == "user@example.com"


def test_decode_token_invalid_returns_none():
    assert decode_token("not-a-real-token") is None
