from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Body
from sqlalchemy.orm import Session
from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.utils.auth.auth_utils import get_password_hash, is_strong_password
from app.utils.token import create_password_reset_token, verify_password_reset_token
from app.utils.email.email_core import send_email_async
import os

router = APIRouter(
    prefix="/auth/password",
    tags=["auth-password"]
)

@router.post("/forgot", summary="Şifremi unuttum: e-posta ile sıfırlama bağlantısı gönder")
def forgot_password(
    email: str = Body(..., embed=True, example="test@chameleonvpn.app"),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    user = db.query(User).filter(User.email == email).first()
    if user:
        token = create_password_reset_token(user.email)
        reset_url = os.getenv("PASSWORD_RESET_URL", "http://localhost:8000/auth/password/reset") + f"?token={token}"
        if background_tasks:
            background_tasks.add_task(
                send_email_async, user.email, "Şifre Sıfırlama", reset_url
            )
    # Güvenlik gereği: her zaman aynı cevap!
    return {"msg": "If registered, a reset link will be sent."}

@router.post("/reset", summary="Token ile yeni şifre belirle")
def reset_password(
    token: str = Body(..., embed=True),
    new_password: str = Body(..., embed=True),
    db: Session = Depends(get_db)
):
    email = verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not is_strong_password(new_password):
        raise HTTPException(status_code=400, detail="Weak password")
    user.password_hash = get_password_hash(new_password)
    db.commit()
    return {"msg": "Password reset successful."}
