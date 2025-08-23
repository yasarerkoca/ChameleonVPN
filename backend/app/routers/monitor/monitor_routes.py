from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
import logging
from app.utils.db.db_utils import get_db

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/monitor",
    tags=["monitor"]
)

@router.get("/health", summary="Uygulama çalışıyor mu?")
def health_check():
    """
    Temel canlılık testi. Load balancer ve dış servisler için kullanılabilir.
    """
    return {"status": "ok"}

@router.get("/db", summary="Veritabanı bağlantı sağlığı kontrolü")
def db_check(db: Session = Depends(get_db)):
    """
    Veritabanı bağlantısının ve okuma yeteneğinin sağlığını kontrol eder.
    """
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except SQLAlchemyError as exc:
        logger.error("Database health check failed: %s", exc)
        return {"status": "db_error", "detail": str(exc)}
