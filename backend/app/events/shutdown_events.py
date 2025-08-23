from fastapi_limiter import FastAPILimiter
from sqlalchemy.exc import SQLAlchemyError
from app.config.database import SessionLocal, engine
from app.logs.logger import logger

def register_shutdown_events(app):
    @app.on_event("shutdown")
    async def _shutdown():
        logger.info("🛑 ChameleonVPN shutting down...")

        # Close Redis rate limiter connection
        try:
            await FastAPILimiter.close()
            logger.info("✅ Redis connection closed")
        except Exception as e:
            logger.error(f"❌ Failed to close Redis connection: {e}")

        # Dispose of database sessions and connections
        try:
            SessionLocal.close_all()
            engine.dispose()
            logger.info("✅ Database connections closed")
        except SQLAlchemyError as e:
            logger.error(f"❌ Failed to close database connections: {e}")

        logger.info("🧹 Cleanup completed")
