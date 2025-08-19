from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.deps import require_role

router = APIRouter(
    prefix="/admin/status-management",
    tags=["admin-status-management"]
)

@router.get("/health", summary="Sistem sağlık durumu (basic)")
def system_health(
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
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
