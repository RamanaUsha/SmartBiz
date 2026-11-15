from sqlalchemy.orm import Session

from app.models.audit_log_db import AuditLogDB


def create_audit_log(
    db: Session,
    file_name: str,
    operations: list,
    comparison: dict
):
    audit_log = AuditLogDB(
        file_name=file_name,
        operations=operations,
        original_rows=comparison["original_rows"],
        cleaned_rows=comparison["cleaned_rows"],
        rows_removed=comparison["rows_removed"],
        cells_changed=comparison["cells_changed"]
    )

    db.add(audit_log)
    db.commit()
    db.refresh(audit_log)

    return audit_log


def get_audit_logs(db: Session):
    return (
        db.query(AuditLogDB)
        .order_by(AuditLogDB.created_at.desc())
        .all()
    )