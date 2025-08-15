from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime, timedelta

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional
from app.models.logs.anomaly_fraud_record import AnomalyFraudRecord
from app.models.user import User
from app.services.anomaly_detector import run_deep_anomaly_analysis

router = APIRouter(
    prefix="/admin/anomaly-analysis",
    tags=["admin-anomaly-analysis"]
)

def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not getattr(current_user, "is_admin", False):
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

@router.get("/logs", summary="Tüm anomaly kayıtlarını getir")
def get_all_anomalies(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    return db.query(AnomalyFraudRecord).order_by(AnomalyFraudRecord.created_at.desc()).all()

@router.get("/logs/recent", summary="Son 48 saatlik anomaly kayıtları")
def recent_anomalies(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    threshold = datetime.utcnow() - timedelta(hours=48)
    return db.query(AnomalyFraudRecord).filter(
        AnomalyFraudRecord.created_at >= threshold
    ).order_by(AnomalyFraudRecord.created_at.desc()).all()

@router.get("/logs/deep-analysis", summary="AI destekli anomaly analiz (detaylı)")
def deep_anomaly_analysis(
    limit: Optional[int] = 500,
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    recent_records = db.query(AnomalyFraudRecord).order_by(
        AnomalyFraudRecord.created_at.desc()
    ).limit(limit).all()

    # AI fonksiyonu dict listesi beklediği için, objeleri dict'e çeviriyoruz.
    log_dicts = [
        {
            "user_id": x.user_id,
            "traffic_mb": getattr(x, "traffic_mb", 0),
            "connect_count": getattr(x, "connect_count", 0)
        }
        for x in recent_records
    ]

    result = run_deep_anomaly_analysis(log_dicts)
    return {"deep_anomaly_results": result}
