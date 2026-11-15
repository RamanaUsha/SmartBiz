
from io import BytesIO

import pandas as pd


def get_auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "email": "spreadsheet-test@example.com",
            "password": "SecurePass123!"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "spreadsheet-test@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def create_csv_file():
    content = (
        "name,email,city\n"
        "Usha,usha@gmail.com,Chittoor\n"
        "Ravi,ravi.gmail.com,Hyderabad\n"
        "Usha,usha@gmail.com,Chittoor\n"
        "Anu,,Bangalore\n"
    )

    return {
        "file": (
            "test_customers.csv",
            BytesIO(content.encode("utf-8")),
            "text/csv"
        )
    }


def create_excel_file():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi"],
        "email": ["usha@gmail.com", "ravi@gmail.com"],
        "city": ["Chittoor", "Hyderabad"]
    })

    buffer = BytesIO()

    dataframe.to_excel(
        buffer,
        index=False,
        engine="openpyxl"
    )

    buffer.seek(0)

    return {
        "file": (
            "test_customers.xlsx",
            buffer,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    }


def test_upload_csv_successfully(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/spreadsheets/upload",
        headers=headers,
        files=create_csv_file()
    )

    assert response.status_code == 200

    result = response.json()

    assert result["message"] == "Spreadsheet processed successfully"
    assert result["overview"]["total_rows"] == 4
    assert result["overview"]["total_columns"] == 3
    assert result["missing_value_report"]["total_missing_values"] == 1
    assert result["duplicate_report"]["duplicate_count"] == 1
    assert result["invalid_email_report"]["invalid_email_count"] == 1
    assert result["data_quality_score"] == 81.67


def test_upload_excel_successfully(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/spreadsheets/upload",
        headers=headers,
        files=create_excel_file()
    )

    assert response.status_code == 200

    result = response.json()

    assert result["message"] == "Spreadsheet processed successfully"
    assert result["overview"]["total_rows"] == 2
    assert result["data_quality_score"] == 100.0


def test_upload_unsupported_file_format(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/spreadsheets/upload",
        headers=headers,
        files={
            "file": (
                "test.txt",
                BytesIO(b"Hello SmartBiz"),
                "text/plain"
            )
        }
    )

    assert response.status_code == 400
    assert "Unsupported file format" in response.json()["detail"]


def test_upload_empty_file(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/spreadsheets/upload",
        headers=headers,
        files={
            "file": (
                "empty.csv",
                BytesIO(b""),
                "text/csv"
            )
        }
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The uploaded file is empty"


def test_upload_file_with_missing_columns(client):
    headers = get_auth_headers(client)

    content = (
        "name,city\n"
        "Usha,Chittoor\n"
        "Ravi,Hyderabad\n"
    )

    response = client.post(
        "/spreadsheets/upload",
        headers=headers,
        files={
            "file": (
                "missing_columns.csv",
                BytesIO(content.encode("utf-8")),
                "text/csv"
            )
        }
    )

    assert response.status_code == 400
    assert "Missing required columns" in response.json()["detail"]


def test_upload_file_exceeding_size_limit(client):
    headers = get_auth_headers(client)

    large_content = b"a" * (5 * 1024 * 1024 + 1)

    response = client.post(
        "/spreadsheets/upload",
        headers=headers,
        files={
            "file": (
                "large.csv",
                BytesIO(large_content),
                "text/csv"
            )
        }
    )

    assert response.status_code == 413
    assert "5 MB" in response.json()["detail"]


def test_upload_without_token(client):
    response = client.post(
        "/spreadsheets/upload",
        files=create_csv_file()
    )

    assert response.status_code == 401
