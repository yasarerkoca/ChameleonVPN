from sqlalchemy.orm import Session
from app.logs.logger import logger
from app.config.database import SessionLocal
from app.deps import seed_default_roles

def register_startup_events(app):
    @app.on_event("startup")
    async def _startup():
        logger.info("✅ Startup event registered")
        db: Session = SessionLocal()
        try:
            seed_default_roles(db)
        finally:
            db.close()
