
import pandas as pd


def compare_dataframes(
    original_dataframe: pd.DataFrame,
    cleaned_dataframe: pd.DataFrame
):
    """
    Compare original and cleaned DataFrames.

    Reports row counts, removed rows, column counts,
    and the number of modified cells.
    """

    if not original_dataframe.index.is_unique:
        raise ValueError("Original DataFrame must have unique row indexes")

    if not cleaned_dataframe.index.is_unique:
        raise ValueError("Cleaned DataFrame must have unique row indexes")

    if not original_dataframe.columns.equals(cleaned_dataframe.columns):
        raise ValueError(
            "Original and cleaned DataFrames must have the same columns"
        )

    if not cleaned_dataframe.index.isin(original_dataframe.index).all():
        raise ValueError(
            "Cleaned DataFrame contains rows not present in the original"
        )

    original_rows = len(original_dataframe)
    cleaned_rows = len(cleaned_dataframe)

    removed_rows = original_rows - cleaned_rows

    retained_original = original_dataframe.loc[
        cleaned_dataframe.index
    ]

    same_values = (
        retained_original.eq(cleaned_dataframe)
        | (
            retained_original.isna()
            & cleaned_dataframe.isna()
        )
    )

    changed_cells = int(
        (~same_values.fillna(False)).to_numpy().sum()
    )

    return {
        "original_rows": original_rows,
        "cleaned_rows": cleaned_rows,
        "rows_removed": removed_rows,
        "original_columns": len(original_dataframe.columns),
        "cleaned_columns": len(cleaned_dataframe.columns),
        "cells_changed": changed_cells
    }
