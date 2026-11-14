
from io import BytesIO

import pandas as pd
import pytest
from app.services.data_cleaning_service import clean_whitespace
from app.services.spreadsheet_service import read_spreadsheet
from app.services.data_cleaning_service import detect_missing_values
from app.services.data_cleaning_service import detect_duplicates
from app.services.data_cleaning_service import detect_invalid_emails

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
