
import pandas as pd

from app.services.data_cleaning_service import (
    detect_missing_values,
    detect_duplicates,
    detect_invalid_emails
)


def generate_data_overview(dataframe: pd.DataFrame):
    """
    Generate a basic overview of spreadsheet data.
    """

    return {
        "total_rows": len(dataframe),
        "total_columns": len(dataframe.columns),
        "column_names": dataframe.columns.tolist()
    }


def generate_missing_value_report(dataframe: pd.DataFrame):
    """
    Generate a report showing missing values in each column.
    """

    missing_values = detect_missing_values(dataframe)

    return {
        "missing_values": missing_values,
        "total_missing_values": sum(missing_values.values())
    }


def generate_duplicate_report(
    dataframe: pd.DataFrame,
    columns: list[str]
):
    """
    Generate a report showing duplicate records.
    """

    duplicate_rows = detect_duplicates(dataframe, columns)

    return {
        "duplicate_count": len(duplicate_rows),
        "duplicate_rows": duplicate_rows.to_dict(orient="records")
    }


def generate_invalid_email_report(
    dataframe: pd.DataFrame,
    email_column: str
):
    """
    Generate a report showing invalid email addresses.
    """

    invalid_emails = detect_invalid_emails(
        dataframe,
        email_column
    )

    return {
        "invalid_email_count": len(invalid_emails),
        "invalid_email_rows": invalid_emails.to_dict(
            orient="records"
        )
    }


def calculate_data_quality_score(
    dataframe: pd.DataFrame,
    duplicate_columns: list[str],
    email_column: str
):
    """
    Calculate an overall data quality score from 0 to 100.

    Weights:
    - Missing values: 40%
    - Duplicate records: 30%
    - Invalid emails: 30%
    """

    if dataframe.empty or len(dataframe.columns) == 0:
        raise ValueError(
            "Cannot calculate score for an empty spreadsheet"
        )

    total_cells = dataframe.size
    total_rows = len(dataframe)

    missing_count = sum(
        detect_missing_values(dataframe).values()
    )

    duplicate_count = len(
        detect_duplicates(dataframe, duplicate_columns)
    )

    invalid_email_count = len(
        detect_invalid_emails(dataframe, email_column)
    )

    missing_rate = missing_count / total_cells
    duplicate_rate = duplicate_count / total_rows
    invalid_email_rate = invalid_email_count / total_rows

    penalty = (
        missing_rate * 40
        + duplicate_rate * 30
        + invalid_email_rate * 30
    )

    score = round(max(0, 100 - penalty), 2)

    return score
