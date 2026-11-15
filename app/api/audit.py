from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user_db import UserDB
from app.services.audit_log_service import get_audit_logs
from app.utils.auth import get_current_user


router = APIRouter(
    tags=["Audit Logs"]
)


@router.get("/audit-logs")
def list_audit_logs(
    db: Session = Depends(get_db),
    current_user: UserDB = Depends(get_current_user)
):
    logs = get_audit_logs(db)

    return {
        "total_records": len(logs),
        "audit_logs": [
            {
                "audit_id": log.audit_id,
                "file_name": log.file_name,
                "operations": log.operations,
                "original_rows": log.original_rows,
                "cleaned_rows": log.cleaned_rows,
                "rows_removed": log.rows_removed,
                "cells_changed": log.cells_changed,
                "created_at": log.created_at
            }
            for log in logs
        ]
    }