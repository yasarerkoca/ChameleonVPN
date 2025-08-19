from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
import secrets
from app.models.security.api_key import APIKey
from app.models.security.api_key_access_log import APIKeyAccessLog
from app.utils.db.db_utils import get_db
from app.models.user import User
from app.deps import require_role

router = APIRouter(
    prefix="/admin/api-keys",
    tags=["admin-api-keys"]
)

@router.post("/create", summary="Yeni API Key oluştur")
def create_api_key(
    user_id: Optional[int] = None,
    corporate_group_id: Optional[int] = None,
    description: str = "",
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    key = secrets.token_urlsafe(32)
    api_key = APIKey(
        key=key,
        user_id=user_id,
        corporate_group_id=corporate_group_id,
        description=description
    )
    db.add(api_key)
    db.commit()
    return {"api_key": key}

@router.get("/list", summary="API Key listesini getir")
def list_api_keys(
    user_id: Optional[int] = None,
    corporate_group_id: Optional[int] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    query = db.query(APIKey)
    if user_id:
        query = query.filter(APIKey.user_id == user_id)
    if corporate_group_id:
        query = query.filter(APIKey.corporate_group_id == corporate_group_id)
    return query.order_by(APIKey.created_at.desc()).all()

@router.delete("/{api_key_id}", summary="API Key sil")
def delete_api_key(api_key_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    api_key = db.query(APIKey).get(api_key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")
    db.delete(api_key)
    db.commit()
    return {"msg": "API Key silindi."}

@router.post("/deactivate/{api_key_id}", summary="API Key devre dışı bırak")
def deactivate_api_key(api_key_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    api_key = db.query(APIKey).get(api_key_id)
    if not api_key:
        raise HTTPException(status_code=404, detail="API Key not found")
    api_key.is_active = False
    db.commit()
    return {"msg": "API Key devre dışı bırakıldı."}

@router.post("/unblock/{api_key_id}", summary="API Key engelini kaldır")
def unblock_api_key(api_key_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    key = db.query(APIKey).get(api_key_id)
    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")
    key.is_blocked = False
    key.last_blocked_at = None
    db.commit()
    return {"msg": "API Key tekrar aktif edildi."}

@router.get("/status/{api_key_id}", summary="API Key durum bilgisi getir")
def api_key_status(api_key_id: int, db: Session = Depends(get_db), _: User = Depends(require_role("admin"))):
    key = db.query(APIKey).get(api_key_id)
    if not key:
        raise HTTPException(status_code=404, detail="API Key not found")
    return {
        "id": key.id,
        "key": key.key,
        "rate_limit_per_minute": key.rate_limit_per_minute,
        "is_active": key.is_active,
        "is_blocked": key.is_blocked,
        "last_blocked_at": key.last_blocked_at
    }

@router.get("/access-logs", summary="API Key kullanım loglarını getir")
def api_key_access_logs(
    api_key_id: Optional[int] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    _: User = Depends(require_role("admin"))
):
    query = db.query(APIKeyAccessLog)
    if api_key_id:
        query = query.filter(APIKeyAccessLog.api_key_id == api_key_id)
    if start_date:
        query = query.filter(APIKeyAccessLog.accessed_at >= start_date)
    if end_date:
        query = query.filter(APIKeyAccessLog.accessed_at <= end_date)
    return query.order_by(APIKeyAccessLog.accessed_at.desc()).all()
