# app.utils.oauth.google_oauth_utils - Google OAuth doğrulama yardımcıları

import os
import requests
from sqlalchemy.orm import Session
from app.models.user.user import User
from typing import Optional
import logging

logger = logging.getLogger(__name__)

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


def verify_google_token(id_token: str) -> Optional[dict]:
    """
    Google ID token'ı doğrular ve geçerli ise payload'u döner.

    Args:
        id_token (str): Google tarafından verilen JWT token

    Returns:
        Optional[dict]: Token içeriği (email, name, vs.)
    """
    try:
        response = requests.get(
            "https://oauth2.googleapis.com/tokeninfo",
            params={"id_token": id_token},
            timeout=5
        )
        if response.status_code != 200:
            logger.warning(f"Google token doğrulama başarısız: {response.status_code}")
            return None

        token_info = response.json()
        if token_info.get("aud") != GOOGLE_CLIENT_ID:
            logger.warning("Google token client ID eşleşmiyor.")
            return None

        return token_info
    except Exception as e:
        logger.error(f"Google token doğrulama hatası: {str(e)}")
        return None


def get_user_from_google_token(id_token: str, db: Session) -> Optional[User]:
    """
    Google token doğrulamasına göre kullanıcıyı döner. Yoksa kayıt eder.

    Args:
        id_token (str): Google ID token
        db (Session): SQLAlchemy DB oturumu

    Returns:
        Optional[User]: Kullanıcı nesnesi (mevcut ya da yeni)
    """
    token_info = verify_google_token(id_token)
    if not token_info:
        return None

    email = token_info.get("email")
    if not email:
        return None

    user = db.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            email=email,
            full_name=token_info.get("name", ""),
            is_active=True,
            is_verified=True
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        logger.info(f"Yeni Google kullanıcısı oluşturuldu: {email}")
    return user
