
import re
import pandas as pd


def detect_missing_values(dataframe: pd.DataFrame):
    """Detect missing values in each column."""
    missing_values = dataframe.isnull().sum()
    return missing_values.to_dict()


def clean_whitespace(dataframe: pd.DataFrame):
    """Trim unnecessary spaces and convert blank text to missing values."""
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
    """Detect duplicate records using selected columns."""
    for column in columns:
        if column not in dataframe.columns:
            raise ValueError(
                f"Column '{column}' does not exist in the spreadsheet"
            )

    return dataframe[
        dataframe.duplicated(subset=columns, keep="first")
    ]


def detect_invalid_emails(dataframe: pd.DataFrame, email_column: str):
    """Detect rows containing invalid email addresses."""
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


def clean_dataframe(
    dataframe: pd.DataFrame,
    trim_whitespace: bool = True,
    remove_duplicates: bool = False,
    duplicate_columns: list[str] | None = None,
    fill_missing_values: dict | None = None
):
    """
    Apply configurable cleaning operations to a spreadsheet.

    The original DataFrame is never modified.
    """

    cleaned_dataframe = dataframe.copy()

    if trim_whitespace:
        cleaned_dataframe = clean_whitespace(cleaned_dataframe)

    if fill_missing_values:
        cleaned_dataframe = cleaned_dataframe.fillna(
            value=fill_missing_values
        )

    if remove_duplicates:
        if not duplicate_columns:
            raise ValueError(
                "Specify duplicate_columns when removing duplicates"
            )

        for column in duplicate_columns:
            if column not in cleaned_dataframe.columns:
                raise ValueError(
                    f"Column '{column}' does not exist in the spreadsheet"
                )

        cleaned_dataframe = cleaned_dataframe.drop_duplicates(
            subset=duplicate_columns,
            keep="first"
        )

    return cleaned_dataframe
