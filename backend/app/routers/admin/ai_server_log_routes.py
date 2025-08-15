from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_admin
from app.models.logs.ai_server_selection_log import AIServerSelectionLog
from app.schemas.logs.ai_server_selection_log import AIServerSelectionLogOut

router = APIRouter(
    prefix="/admin/ai-selection-log",
    tags=["admin-ai-selection-log"]
)

@router.get("/", response_model=List[AIServerSelectionLogOut], summary="AI sunucu seçim loglarını getir")
def get_ai_logs(
    db: Session = Depends(get_db),
    current_admin=Depends(get_current_admin)
):
    logs = db.query(AIServerSelectionLog).order_by(AIServerSelectionLog.created_at.desc()).limit(100).all()
    return logs
