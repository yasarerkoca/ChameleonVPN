# ~/ChameleonVPN/backend/app/routers/vpn/__init__.py

from fastapi import APIRouter

from .activity_routes import router as activity_router
from .ai_selector_routes import router as ai_selector_router
from .config_routes import router as config_router
from .server_routes import router as server_router
from .status_routes import router as status_router
from .traffic_routes import router as traffic_router
from .quota_routes import router as quota_router
from .connection_routes import router as connection_router  # << bu önemli
from .vpn_peers import router as peer_router

router = APIRouter()

router.include_router(activity_router)
router.include_router(ai_selector_router)
router.include_router(config_router)
router.include_router(server_router)
router.include_router(status_router)
router.include_router(traffic_router)
router.include_router(quota_router)
router.include_router(connection_router)
router.include_router(peer_router)
