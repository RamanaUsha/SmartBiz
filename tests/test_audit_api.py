from app.services.audit_log_service import create_audit_log


def test_get_audit_logs_api(client, db_session):
    comparison = {
        "original_rows": 10,
        "cleaned_rows": 8,
        "rows_removed": 2,
        "cells_changed": 3
    }

    create_audit_log(
        db=db_session,
        file_name="customers.xlsx",
        operations=["trim_whitespace", "remove_duplicates"],
        comparison=comparison
    )

    response = client.get("/audit-logs")

    assert response.status_code == 200

    data = response.json()

    assert data["total_records"] == 1
    assert len(data["audit_logs"]) == 1

    audit_log = data["audit_logs"][0]

    assert audit_log["file_name"] == "customers.xlsx"
    assert audit_log["original_rows"] == 10
    assert audit_log["cleaned_rows"] == 8
    assert audit_log["rows_removed"] == 2
    assert audit_log["cells_changed"] == 3


def test_get_empty_audit_logs_api(client):
    response = client.get("/audit-logs")

    assert response.status_code == 200
    assert response.json()["total_records"] == 0
    assert response.json()["audit_logs"] == []