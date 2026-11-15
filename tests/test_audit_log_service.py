from app.services.audit_log_service import (
    create_audit_log,
    get_audit_logs
)


def test_create_audit_log(db_session):
    comparison = {
        "original_rows": 10,
        "cleaned_rows": 8,
        "rows_removed": 2,
        "cells_changed": 3
    }

    result = create_audit_log(
        db=db_session,
        file_name="customers.xlsx",
        operations=["trim_whitespace", "remove_duplicates"],
        comparison=comparison
    )

    assert result.audit_id is not None
    assert result.file_name == "customers.xlsx"
    assert result.operations == [
        "trim_whitespace",
        "remove_duplicates"
    ]
    assert result.original_rows == 10
    assert result.cleaned_rows == 8
    assert result.rows_removed == 2
    assert result.cells_changed == 3


def test_get_audit_logs(db_session):
    comparison = {
        "original_rows": 5,
        "cleaned_rows": 4,
        "rows_removed": 1,
        "cells_changed": 2
    }

    create_audit_log(
        db=db_session,
        file_name="test_customers.csv",
        operations=["trim_whitespace"],
        comparison=comparison
    )

    logs = get_audit_logs(db_session)

    assert len(logs) == 1
    assert logs[0].file_name == "test_customers.csv"