
from io import BytesIO

from app.services.audit_log_service import get_audit_logs


def test_clean_spreadsheet_creates_audit_log(client, db_session):
    content = (
        "name,email,city\n"
        " Usha ,usha@gmail.com,Chittoor\n"
        "Ravi,ravi@gmail.com,Hyderabad\n"
        "Usha,usha@gmail.com,Chittoor\n"
    )

    response = client.post(
        "/spreadsheets/clean-and-download",
        params={"remove_duplicates": "true"},
        files={
            "file": (
                "customers.csv",
                BytesIO(content.encode("utf-8")),
                "text/csv"
            )
        }
    )

    assert response.status_code == 200
    assert "spreadsheetml.sheet" in response.headers["content-type"]

    logs = get_audit_logs(db_session)

    assert len(logs) == 1

    audit_log = logs[0]

    assert audit_log.file_name == "customers.csv"
    assert audit_log.original_rows == 3
    assert audit_log.cleaned_rows == 2
    assert audit_log.rows_removed == 1
    assert audit_log.operations == [
        "trim_whitespace",
        "remove_duplicates"
    ]


def test_clean_spreadsheet_without_duplicates(client, db_session):
    content = (
        "name,email\n"
        " Usha ,usha@gmail.com\n"
        "Ravi,ravi@gmail.com\n"
    )

    response = client.post(
        "/spreadsheets/clean-and-download",
        files={
            "file": (
                "customers.csv",
                BytesIO(content.encode("utf-8")),
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    logs = get_audit_logs(db_session)

    assert len(logs) == 1
    assert logs[0].rows_removed == 0
    assert logs[0].operations == ["trim_whitespace"]
