from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app import models, schemas, auth, utils

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

def send_verification_email(user):
    # Burayı gerçek e-posta gönderim sistemi ile değiştirmen gerekir
    print(f"Verification email sent to: {user.email}")

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(utils.get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    if not auth.is_strong_password(user.password):
        raise HTTPException(status_code=400, detail="Password is too weak")

    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        is_active=True,  # Geliştirme sürecinde aktif olsun
        email_verified=True  # Geliştirme sürecinde doğrulanmış kabul et
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    send_verification_email(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(utils.get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")

    if not user.is_active or not user.email_verified:
        raise HTTPException(status_code=403, detail="Account is not activated")

    access_token = auth.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
