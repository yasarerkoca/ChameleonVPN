# ~/ChameleonVPN/backend/app/routers/auth/firebase_routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config.database import get_db
from app.services.auth.firebase import verify_id_token, get_or_create_user_from_firebase

# JWT üretimi (mevcut projenizdeki doğru importu kullanın)
from app.services.auth.jwt import create_access_token, create_refresh_token  # isimleri uyarlayın

router = APIRouter(prefix="/auth/firebase", tags=["auth"])

class FirebaseLoginIn(BaseModel):
    id_token: str

class TokenOut(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenOut)
def firebase_login(body: FirebaseLoginIn, db: Session = Depends(get_db)):
    try:
        payload = verify_id_token(body.id_token)
        _, user_id = get_or_create_user_from_firebase(db, payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    access = create_access_token({"sub": str(user_id)})
    refresh = create_refresh_token({"sub": str(user_id)})
    return TokenOut(access_token=access, refresh_token=refresh)
