# ~/ChameleonVPN/backend/app/routers/health.py
from fastapi import APIRouter
router = APIRouter()
@router.get("/healthz")
def healthz():
    return {"ok": True}
