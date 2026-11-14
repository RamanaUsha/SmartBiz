
from io import BytesIO

import pandas as pd
import pytest
from app.services.data_cleaning_service import clean_whitespace
from app.services.spreadsheet_service import read_spreadsheet
from app.services.data_cleaning_service import detect_missing_values
from app.services.data_cleaning_service import detect_duplicates
from app.services.data_cleaning_service import detect_invalid_emails
from app.services.excel_export_service import export_cleaned_excel

def test_read_csv_file():
    content = b"name,email\nUsha,usha@gmail.com\n"

    dataframe = read_spreadsheet("customers.csv", content)

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["name"] == "Usha"
    assert dataframe.iloc[0]["email"] == "usha@gmail.com"


def test_read_excel_file():
    buffer = BytesIO()

    pd.DataFrame({
        "name": ["Usha"],
        "email": ["usha@gmail.com"]
    }).to_excel(buffer, index=False)

    dataframe = read_spreadsheet(
        "customers.xlsx",
        buffer.getvalue()
    )

    assert len(dataframe) == 1
    assert dataframe.iloc[0]["name"] == "Usha"
    assert dataframe.iloc[0]["email"] == "usha@gmail.com"


def test_unsupported_file_format():
    with pytest.raises(ValueError):
        read_spreadsheet("customers.pdf", b"sample content")
def test_detect_missing_values():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi", None],
        "email": ["usha@gmail.com", None, "ravi@gmail.com"]
    })

    result = detect_missing_values(dataframe)

    assert result["name"] == 1
    assert result["email"] == 1
def test_clean_whitespace():
    dataframe = pd.DataFrame({
        "name": [" Usha ", " Ravi "],
        "email": [" usha@gmail.com ", "   "]
    })

    cleaned = clean_whitespace(dataframe)

    assert cleaned.iloc[0]["name"] == "Usha"
    assert cleaned.iloc[0]["email"] == "usha@gmail.com"
    assert cleaned.iloc[1]["name"] == "Ravi"
    assert pd.isna(cleaned.iloc[1]["email"])

    # Original data must remain unchanged.
    assert dataframe.iloc[0]["name"] == " Usha "

def test_detect_duplicates():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi", "Usha"],
        "email": [
            "usha@gmail.com",
            "ravi@gmail.com",
            "usha@gmail.com"
        ]
    })

    duplicates = detect_duplicates(dataframe, ["email"])

    assert len(duplicates) == 1
    assert duplicates.iloc[0]["name"] == "Usha"
    assert duplicates.iloc[0]["email"] == "usha@gmail.com"


def test_detect_duplicates_invalid_column():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi"]
    })

    with pytest.raises(ValueError):
        detect_duplicates(dataframe, ["email"])
def test_detect_invalid_emails():
    dataframe = pd.DataFrame({
        "email": [
            "usha@gmail.com",
            "usha.gmail.com",
            "usha@",
            None
        ]
    })

    result = detect_invalid_emails(dataframe, "email")

    assert len(result) == 2
    assert result["email"].tolist() == [
        "usha.gmail.com",
        "usha@"
    ]


def test_detect_invalid_emails_missing_column():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi"]
    })

    with pytest.raises(ValueError):
        detect_invalid_emails(dataframe, "email")

from app.services.data_cleaning_service import clean_dataframe


def test_clean_dataframe_trims_whitespace():
    dataframe = pd.DataFrame({
        "name": [" Usha ", " Ravi "],
        "email": [" usha@gmail.com ", " ravi@gmail.com "]
    })

    cleaned = clean_dataframe(dataframe)

    assert cleaned["name"].tolist() == ["Usha", "Ravi"]
    assert cleaned["email"].tolist() == [
        "usha@gmail.com",
        "ravi@gmail.com"
    ]


def test_clean_dataframe_removes_duplicates():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi", "Usha"],
        "email": [
            "usha@gmail.com",
            "ravi@gmail.com",
            "usha@gmail.com"
        ]
    })

    cleaned = clean_dataframe(
        dataframe,
        remove_duplicates=True,
        duplicate_columns=["email"]
    )

    assert len(cleaned) == 2


def test_clean_dataframe_fills_missing_values():
    dataframe = pd.DataFrame({
        "name": ["Usha", None],
        "city": ["Chittoor", None]
    })

    cleaned = clean_dataframe(
        dataframe,
        fill_missing_values={
            "name": "Unknown",
            "city": "Not Provided"
        }
    )

    assert cleaned["name"].tolist() == ["Usha", "Unknown"]
    assert cleaned["city"].tolist() == [
        "Chittoor",
        "Not Provided"
    ]


def test_clean_dataframe_preserves_original():
    dataframe = pd.DataFrame({
        "name": [" Usha ", " Usha "],
        "email": ["usha@gmail.com", "usha@gmail.com"]
    })

    original = dataframe.copy(deep=True)

    clean_dataframe(
        dataframe,
        remove_duplicates=True,
        duplicate_columns=["email"]
    )

    pd.testing.assert_frame_equal(dataframe, original)

def test_export_cleaned_excel_successfully():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi"],
        "email": ["usha@gmail.com", "ravi@gmail.com"]
    })

    excel_content = export_cleaned_excel(dataframe)

    assert isinstance(excel_content, bytes)
    assert len(excel_content) > 0

    exported_dataframe = pd.read_excel(
        BytesIO(excel_content),
        engine="openpyxl"
    )

    assert exported_dataframe["name"].tolist() == ["Usha", "Ravi"]
    assert exported_dataframe["email"].tolist() == [
        "usha@gmail.com",
        "ravi@gmail.com"
    ]


def test_export_cleaned_excel_preserves_columns():
    dataframe = pd.DataFrame({
        "name": ["Usha"],
        "email": ["usha@gmail.com"],
        "city": ["Chittoor"]
    })

    excel_content = export_cleaned_excel(dataframe)

    exported_dataframe = pd.read_excel(
        BytesIO(excel_content),
        engine="openpyxl"
    )

    assert exported_dataframe.columns.tolist() == [
        "name",
        "email",
        "city"
    ]
