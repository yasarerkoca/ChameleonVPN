from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional
from app.models.user.user import User

router = APIRouter(
    prefix="/admin/status-management",
    tags=["admin-status-management"]
)

def admin_required(current_user: User = Depends(get_current_user_optional)):
    # Dilersen bu kontrole Swagger UI testlerinde disable yapabilirsin.
    if not current_user or not current_user.is_admin:
        return {"status": "unauthorized"}
    return current_user

@router.get("/health", summary="Sistem sağlık durumu (basic)")
def system_health(
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    # Basit bir veritabanı bağlantı kontrolüyle sağlığı ölç
    try:
        db.execute("SELECT 1")
        db_status = "ok"
    except Exception:
        db_status = "unreachable"

    # Buraya başka sağlık kontrolleri (cache, servis, disk vs.) de eklenebilir.
    return {
        "status": "ok" if db_status == "ok" else "problem",
        "database": db_status,
        "version": "1.0.0"
    }
