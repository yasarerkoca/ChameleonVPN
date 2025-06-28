
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, auth, utils, email_utils
from app.auth import create_access_token, create_refresh_token, get_password_hash, verify_password, generate_token, revoke_token
from app.utils import get_db
from datetime import datetime, timedelta
import asyncio
router = APIRouter(prefix="/auth", tags=["auth"])
async def send_verification_email(email, token):
    subject = "ChameleonVPN Hesap Aktivasyonu"
    body = f"Emailinizi doğrulamak için şu linke tıklayın: https://frontend.com/activate/{token}"
    await email_utils.send_email_async(email, subject, body)
@router.post("/register", response_model=schemas.UserOut)
async def register(user: schemas.UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    verify_token = generate_token()
    db_user = models.User(email=user.email, hashed_password=hashed_password, is_active=False, email_verified=False, email_verify_token=verify_token)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    background_tasks.add_task(asyncio.create_task, send_verification_email(db_user.email, verify_token))
    return db_user
@router.get("/verify/{token}")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email_verify_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.is_active = True
    user.email_verified = True
    user.email_verify_token = None
    db.commit()
    return {"detail": "Email verified, you can login now."}
@router.post("/login", response_model=schemas.TokenOut)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    if not db_user.is_active or not db_user.email_verified or db_user.is_banned:
        raise HTTPException(status_code=403, detail="Please activate your account via email")
    access_token = create_access_token(data={"sub": db_user.email})
    refresh_token = create_refresh_token(data={"sub": db_user.email})
    db_user.refresh_token = refresh_token
    db_user.last_login = datetime.utcnow()
    db.commit()
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
@router.post("/refresh", response_model=schemas.TokenOut)
def refresh_token_api(refresh_token: str, db: Session = Depends(get_db)):
    try:
        payload = auth.decode_token(refresh_token)
    except:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    user = db.query(models.User).filter(models.User.email == payload.get("sub")).first()
    if not user or user.refresh_token != refresh_token:
        raise HTTPException(status_code=401, detail="Invalid session")
    access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})
    user.refresh_token = new_refresh_token
    db.commit()
    return {"access_token": access_token, "refresh_token": new_refresh_token, "token_type": "bearer"}
@router.post("/logout")
def logout(current_user: models.User = Depends(utils.get_current_user), db: Session = Depends(get_db)):
    revoke_token(current_user.refresh_token)
    current_user.refresh_token = None
    db.commit()
    return {"detail": "Logged out."}
@router.post("/forgot-password")
async def forgot_password(email: str, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    token = generate_token()
    user.reset_token = token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.commit()
    subject = "ChameleonVPN Şifre Sıfırlama"
    body = f"Şifre sıfırlama kodunuz: {token}"
    await email_utils.send_email_async(email, subject, body)
    return {"detail": "Reset token sent via email"}
@router.post("/reset-password")
def reset_password(email: str, token: str, new_password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or user.reset_token != token or user.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    user.hashed_password = get_password_hash(new_password)
    user.reset_token = None
    user.reset_token_expiry = None
    db.commit()
    return {"detail": "Password reset successfully"}
    