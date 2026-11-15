
from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    JSON,
    String
)

from app.database import Base


class AuditLogDB(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    file_name = Column(
        String(255),
        nullable=False
    )

    operations = Column(
        JSON,
        nullable=False
    )

    original_rows = Column(
        Integer,
        nullable=False
    )

    cleaned_rows = Column(
        Integer,
        nullable=False
    )

    rows_removed = Column(
        Integer,
        nullable=False
    )

    cells_changed = Column(
        Integer,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
