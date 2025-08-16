from app.logs.logger import logger

def register_startup_events(app):
    @app.on_event("startup")
    async def _startup():
        logger.info("✅ Startup event registered")
