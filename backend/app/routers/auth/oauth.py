from fastapi import APIRouter, Request, HTTPException, Depends, Body
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from sqlalchemy.orm import Session
from app.crud.user.basic_crud import get_user_by_email, create_user
from app.utils.token import create_access_token
from app.utils.db.db_utils import get_db
from app.utils.oauth.google_oauth_utils import get_user_from_google_token

import os

router = APIRouter(
    prefix="/auth/google",
    tags=["auth-google"]
)

config = Config('.env')

oauth = OAuth(config)
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID", "google-client-id"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET", "google-client-secret"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get('/login', summary="Google OAuth ile giriş başlat (redirect)")
async def login_via_google(request: Request):
    redirect_uri = os.getenv("GOOGLE_OAUTH_CALLBACK_URL", "https://chameleonvpn.app/auth/google/callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/callback', summary="Google OAuth callback endpoint")
async def auth_via_google_callback(request: Request, db: Session = Depends(get_db)):
    try:
        token = await oauth.google.authorize_access_token(request)
        user_info = await oauth.google.parse_id_token(request, token)
        email = user_info.get("email")
        name = user_info.get("name")
        if not email:
            raise HTTPException(status_code=400, detail="Google email alınamadı")
        user = get_user_by_email(db, email)
        if not user:
            user = create_user(db, {"email": email, "password": None, "name": name})
        jwt_token = create_access_token(data={"sub": email, "user_id": user.id})
        return {
            "email": email,
            "name": name,
            "access_token": jwt_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Google OAuth hata: {e}")

@router.post('/token', summary="Google OAuth token doğrula (mobil için)")
async def auth_via_google_token(token: str = Body(..., embed=True), db: Session = Depends(get_db)):
    try:
        user = get_user_from_google_token(token, db)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid Google token or user not found")
        jwt_token = create_access_token(data={"sub": user.email, "user_id": user.id})
        return {"access_token": jwt_token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Google OAuth hata: {e}")
