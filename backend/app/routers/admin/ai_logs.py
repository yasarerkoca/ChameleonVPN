from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional, List

from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional
from app.models.user import User
from app.models.logs.anomaly_fraud_record import AnomalyFraudRecord
from app.models.user.user_activity_log import UserActivityLog
from app.models.proxy.proxy_usage_log import ProxyUsageLog
from app.services.anomaly_detector import detect_anomalies
from app.crud.logs import log_crud

router = APIRouter(
    prefix="/admin/ai-logs",
    tags=["admin-ai-logs"]
)


def admin_required(current_user: User = Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

@router.get("/detect", summary="AI ile anomali tespiti")
def ai_log_analysis(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    logs = log_crud.get_user_log_stats(db)
    anomalies = detect_anomalies(logs)
    return {"anomalies": anomalies}

@router.get("/recent", summary="Son 24 saatlik anomaly kayıtları")
def recent_anomalies(db: Session = Depends(get_db), _: User = Depends(admin_required)):
    since = datetime.utcnow() - timedelta(hours=24)
    results = db.query(AnomalyFraudRecord)\
        .filter(AnomalyFraudRecord.created_at >= since)\
        .order_by(AnomalyFraudRecord.created_at.desc())\
        .all()
    return results


@router.get("/activity/search", summary="Kullanıcı aktivitelerini filtrele")
def search_logs(
    user_id: Optional[int] = None,
    action: Optional[str] = None,
    ip_address: Optional[str] = None,
    start_date: Optional[str] = Query(None, example="2024-01-01T00:00:00"),
    end_date: Optional[str] = Query(None, example="2024-01-02T00:00:00"),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    query = db.query(UserActivityLog)
    if user_id:
        query = query.filter(UserActivityLog.user_id == user_id)
    if action:
        query = query.filter(UserActivityLog.action.ilike(f"%{action}%"))
    if ip_address:
        query = query.filter(UserActivityLog.ip_address == ip_address)
    if start_date:
        query = query.filter(UserActivityLog.created_at >= start_date)
    if end_date:
        query = query.filter(UserActivityLog.created_at <= end_date)
    return query.order_by(UserActivityLog.created_at.desc()).all()


@router.get("/proxy-usage/search", summary="Proxy kullanım geçmişi")
def search_proxy_usage(
    user_id: Optional[int] = None,
    proxy_id: Optional[int] = None,
    start_date: Optional[str] = Query(None, example="2024-01-01T00:00:00"),
    end_date: Optional[str] = Query(None, example="2024-01-02T00:00:00"),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    query = db.query(ProxyUsageLog)
    if user_id:
        query = query.filter(ProxyUsageLog.user_id == user_id)
    if proxy_id:
        query = query.filter(ProxyUsageLog.proxy_id == proxy_id)
    if start_date:
        query = query.filter(ProxyUsageLog.timestamp >= start_date)
    if end_date:
        query = query.filter(ProxyUsageLog.timestamp <= end_date)
    return query.order_by(ProxyUsageLog.timestamp.desc()).all()


@router.get("/anomalies/search", summary="Anomali kayıtlarını filtrele")
def search_anomaly_logs(
    user_id: Optional[int] = None,
    ip_address: Optional[str] = None,
    reason: Optional[str] = None,
    start_date: Optional[str] = Query(None, example="2024-01-01T00:00:00"),
    end_date: Optional[str] = Query(None, example="2024-01-02T00:00:00"),
    db: Session = Depends(get_db),
    _: User = Depends(admin_required)
):
    query = db.query(AnomalyFraudRecord)
    if user_id:
        query = query.filter(AnomalyFraudRecord.user_id == user_id)
    if ip_address:
        query = query.filter(AnomalyFraudRecord.ip_address == ip_address)
    if reason:
        query = query.filter(AnomalyFraudRecord.reason.ilike(f"%{reason}%"))
    if start_date:
        query = query.filter(AnomalyFraudRecord.created_at >= start_date)
    if end_date:
        query = query.filter(AnomalyFraudRecord.created_at <= end_date)
    return query.order_by(AnomalyFraudRecord.created_at.desc()).all()
