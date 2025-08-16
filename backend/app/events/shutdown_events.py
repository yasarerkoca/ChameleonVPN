from app.logs.logger import logger

def register_shutdown_events(app):
    @app.on_event("shutdown")
    async def _shutdown():
        logger.info("🛑 Shutdown event registered")
