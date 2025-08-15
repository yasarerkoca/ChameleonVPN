# app.utils.db.db_utils - Veritabanı bağlantısı yardımcı fonksiyonu

from app.config.database import SessionLocal
from sqlalchemy.orm import Session
from typing import Generator


def get_db() -> Generator[Session, None, None]:
    """
    Her istekte SQLAlchemy veritabanı oturumu oluşturur ve sonunda kapatır.
    
    Returns:
        Generator[Session, None, None]: SQLAlchemy DB oturumu
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
