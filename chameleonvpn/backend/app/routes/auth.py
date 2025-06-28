
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, auth, utils

router = APIRouter(prefix="/auth", tags=["auth"])

def send_verification_email(user):
    # Gerçek bir mail gönderim fonksiyonu yazmanız gerek!
    print(f"Verification mail sent to: {user.email}")

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    if not auth.is_strong_password(user.password):
        raise HTTPException(status_code=400, detail="Password is too weak")
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, is_active=False, email_verified=False)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    send_verification_email(db_user)
    return db_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    db_user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not db_user or not auth.verify_password(form_data.password, db_user.hashed_password):
        print(f"Failed login for {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect credentials")
    if not db_user.is_active or not db_user.email_verified:
        raise HTTPException(status_code=403, detail="Please activate your account via email")
    access_token = auth.create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}
