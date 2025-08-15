import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.models.user.user import User
from app.utils.db.db_utils import get_db
from app.utils.auth.auth_utils import get_current_user_optional

router = APIRouter(
    prefix="/admin/user-csv",
    tags=["admin-user-csv"]
)

def admin_required(current_user=Depends(get_current_user_optional)):
    if not current_user or not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin yetkisi gerekli")
    return current_user

@router.get("/export", summary="Tüm kullanıcıları CSV olarak indir")
def export_users_csv(db: Session = Depends(get_db), _: str = Depends(admin_required)):
    users = db.query(User).all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "email", "full_name", "status", "role", "last_login", "is_active", "is_admin",
        "created_at", "corporate_group_id", "proxy_quota_gb", "active_proxy_count"
    ])
    for user in users:
        writer.writerow([
            user.id,
            user.email,
            getattr(user, "full_name", ""),
            getattr(user, "status", ""),
            getattr(user, "role", ""),
            getattr(user, "last_login", ""),
            user.is_active,
            user.is_admin,
            user.created_at,
            getattr(user, "corporate_group_id", ""),
            getattr(user, "proxy_quota_gb", 0),
            getattr(user, "active_proxy_count", 0)
        ])
    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )

@router.post("/import", summary="CSV ile toplu kullanıcı ekle (import)")
def import_users_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: str = Depends(admin_required)
):
    try:
        content = file.file.read().decode("utf-8").splitlines()
        reader = csv.DictReader(content)
        imported = []
        for row in reader:
            if not row.get("email"):
                continue
            user = User(
                email=row["email"],
                full_name=row.get("full_name", ""),
                status=row.get("status", "active"),
                role=row.get("role", "user"),
                is_active=row.get("is_active", "True") == "True",
                is_admin=row.get("is_admin", "False") == "True",
                created_at=row.get("created_at") or datetime.utcnow(),
                corporate_group_id=row.get("corporate_group_id") or None,
                proxy_quota_gb=int(row.get("proxy_quota_gb", 0)),
                active_proxy_count=int(row.get("active_proxy_count", 0)),
            )
            db.add(user)
            imported.append(row["email"])
        db.commit()
        return {"msg": f"{len(imported)} kullanıcı import edildi.", "imported": imported}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {e}")
