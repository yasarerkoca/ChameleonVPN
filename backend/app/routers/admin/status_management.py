from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.utils.db.db_utils import get_db
from app.models.user.user import User
from app.deps import require_role

logger = logging.getLogger(__name__)

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
    except SQLAlchemyError as exc:
        logger.error("Database health check failed: %s", exc)
        db_status = "unreachable"
    except Exception as exc:
        logger.error("Unexpected error during health check: %s", exc)
        db_status = "error"

    # Buraya başka sağlık kontrolleri (cache, servis, disk vs.) de eklenebilir.
    return {
        "status": "ok" if db_status == "ok" else "problem",
        "database": db_status,
        "version": "1.0.0"
    }
