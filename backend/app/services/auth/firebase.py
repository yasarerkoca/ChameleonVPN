# ~/ChameleonVPN/backend/app/services/auth/firebase.py
import os
from typing import Tuple
from sqlalchemy.orm import Session

import firebase_admin
from firebase_admin import auth as fb_auth, credentials

from app.crud.security.identity_provider_crud import get_by_provider_uid, link_user_provider
# Kullanıcı CRUD (mevcut projenizdeki doğru importu kullanın)
from app.crud.user.user_crud import get_user_by_email, create_user  # gerekirse ismi uyarlayın

_project_id = os.getenv("FIREBASE_PROJECT_ID", "chameleonvpn-aba53")
_creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/secrets/serviceAccount.json")

_firebase_app = None
def _ensure_init():
    global _firebase_app
    if _firebase_app is None:
        cred = credentials.Certificate(_creds_path)
        _firebase_app = firebase_admin.initialize_app(cred)

def verify_id_token(id_token: str) -> dict:
    _ensure_init()
    decoded = fb_auth.verify_id_token(id_token, check_revoked=True)
    # Güvenlik: aud/iss kontrolü
    if _project_id and decoded.get("aud") != _project_id:
        raise ValueError("Invalid audience")
    iss = decoded.get("iss", "")
    if _project_id and not iss.endswith(_project_id):
        raise ValueError("Invalid issuer")
    return decoded

def get_or_create_user_from_firebase(db: Session, payload: dict) -> Tuple[dict, int]:
    """
    Dönüş: (payload, user_id)
    """
    provider = (payload.get("firebase", {}).get("sign_in_provider") or "firebase").lower()
    provider_uid = payload.get("uid") or payload.get("sub")
    if not provider_uid:
        raise ValueError("Missing provider UID")

    # 1) Provider bağını kontrol et
    bound = get_by_provider_uid(db, provider, provider_uid)
    if bound:
        return payload, bound.user_id

    email = payload.get("email")
    email_verified = payload.get("email_verified", False)

    # 2) E-posta zorunlu ve verified olsun
    if not email or not email_verified:
        raise ValueError("Email not verified on provider")

    # 3) Var olan kullanıcıya bağla ya da yeni kullanıcı oluştur
    user = get_user_by_email(db, email=email)
    if not user:
        # Yeni kullanıcı: minimum alanlarla oluştur
        user = create_user(
            db,
            email=email,
            password=None,          # sosyal girişte parola olmayabilir
            full_name=payload.get("name") or email.split("@")[0],
            is_active=True,
            is_verified=True,
        )
    link_user_provider(db, user_id=user.id, provider=provider, provider_uid=provider_uid, email=email)
    return payload, user.id
