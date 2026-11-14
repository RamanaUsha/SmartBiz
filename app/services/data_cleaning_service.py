
import pandas as pd
import re

def detect_missing_values(dataframe: pd.DataFrame):
    """
    Detect missing values in each column.
    Return the number of missing values per column.
    """

    missing_values = dataframe.isnull().sum()

    return missing_values.to_dict()

def clean_whitespace(dataframe: pd.DataFrame):
    """
    Remove unnecessary spaces from text columns.
    Convert empty text values into missing values.
    Return a cleaned copy of the DataFrame.
    """

    cleaned_dataframe = dataframe.copy()

    for column in cleaned_dataframe.columns:
        cleaned_dataframe[column] = cleaned_dataframe[column].map(
            lambda value: value.strip()
            if isinstance(value, str)
            else value
        )

        cleaned_dataframe[column] = cleaned_dataframe[column].replace(
            "", pd.NA
        )

    return cleaned_dataframe

def detect_duplicates(dataframe: pd.DataFrame, columns: list[str]):
    """
    Detect duplicate records using selected columns.
    Return the duplicate rows.
    """

    for column in columns:
        if column not in dataframe.columns:
            raise ValueError(
                f"Column '{column}' does not exist in the spreadsheet"
            )

    duplicate_rows = dataframe[
        dataframe.duplicated(subset=columns, keep="first")
    ]

    return duplicate_rows

def detect_invalid_emails(dataframe: pd.DataFrame, email_column: str):
    """
    Detect invalid email addresses in a selected column.
    Return rows containing invalid email values.
    """

    if email_column not in dataframe.columns:
        raise ValueError(
            f"Column '{email_column}' does not exist in the spreadsheet"
        )

    email_pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    invalid_mask = (
        dataframe[email_column].notna()
        & ~dataframe[email_column].astype(str).str.match(email_pattern)
    )

    return dataframe[invalid_mask]
