import csv
import io
from datetime import datetime
from fastapi import APIRouter, Depends, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
import logging

from app.models.user.user import User
from app.utils.db.db_utils import get_db
from app.deps import require_role

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/admin/user-csv",
    tags=["admin-user-csv"]
)


@router.get("/export", summary="Tüm kullanıcıları CSV olarak indir")
def export_users_csv(
    db: Session = Depends(get_db),
    _: str = Depends(require_role("admin"))
):
    users = db.query(User).all()
    output = io.StringIO()
    writer = csv.writer(output)

    # Header
    writer.writerow([
        "id", "email", "full_name", "status", "role", "last_login", "is_active", "is_admin",
        "created_at", "corporate_group_id", "proxy_quota_gb", "active_proxy_count"
    ])

    # Rows
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
            getattr(user, "corporate_group_id", None),
            getattr(user, "proxy_quota_gb", 0),
            getattr(user, "active_proxy_count", 0),
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=users.csv"}
    )


@router.post("/import", summary="CSV dosyasından kullanıcı import et")
def import_users_csv(
    db: Session = Depends(get_db),
    file: UploadFile = File(...),
    _: str = Depends(require_role("admin"))
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

    except SQLAlchemyError as exc:
        db.rollback()
        logger.error("User import failed: %s", exc)
        raise HTTPException(status_code=400, detail=f"Import failed: {exc}")
