from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
import os
import firebase_admin
from firebase_admin import credentials, auth as fb_auth

router = APIRouter(prefix="/auth/firebase", tags=["auth-firebase"])

class FirebaseIdTokenIn(BaseModel):
    id_token: str

def _ensure_fb():
    if not firebase_admin._apps:
        cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "/app/secrets/serviceAccount.json")
        if os.path.exists(cred_path):
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            firebase_admin.initialize_app()

@router.post("/login")
def firebase_login(payload: FirebaseIdTokenIn):
    _ensure_fb()
    try:
        decoded = fb_auth.verify_id_token(payload.id_token)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"Invalid Firebase ID token: {e}")
    return {
        "ok": True,
        "claims": {
            "uid": decoded.get("uid"),
            "email": decoded.get("email"),
            "name": decoded.get("name"),
            "picture": decoded.get("picture"),
            "provider": decoded.get("firebase", {}).get("sign_in_provider"),
        },
    }
