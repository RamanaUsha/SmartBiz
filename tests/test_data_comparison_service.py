
import pandas as pd
import pytest

from app.services.data_comparison_service import compare_dataframes


def test_compare_dataframes_with_changes():
    original = pd.DataFrame({
        "name": [" Usha ", "Ravi", "Usha"],
        "email": [
            "usha@gmail.com",
            "ravi@gmail.com",
            "usha@gmail.com"
        ]
    })

    cleaned = pd.DataFrame({
        "name": ["Usha", "Ravi"],
        "email": [
            "usha@gmail.com",
            "ravi@gmail.com"
        ]
    }, index=[0, 1])

    result = compare_dataframes(original, cleaned)

    assert result["original_rows"] == 3
    assert result["cleaned_rows"] == 2
    assert result["rows_removed"] == 1
    assert result["original_columns"] == 2
    assert result["cleaned_columns"] == 2
    assert result["cells_changed"] == 1


def test_compare_dataframes_without_changes():
    dataframe = pd.DataFrame({
        "name": ["Usha", "Ravi"],
        "email": ["usha@gmail.com", "ravi@gmail.com"]
    })

    result = compare_dataframes(dataframe, dataframe.copy())

    assert result["rows_removed"] == 0
    assert result["cells_changed"] == 0


def test_compare_dataframes_with_missing_values():
    original = pd.DataFrame({
        "name": ["Usha", None]
    })

    cleaned = pd.DataFrame({
        "name": ["Usha", None]
    })

    result = compare_dataframes(original, cleaned)

    assert result["cells_changed"] == 0


def test_compare_dataframes_rejects_different_columns():
    original = pd.DataFrame({
        "name": ["Usha"]
    })

    cleaned = pd.DataFrame({
        "email": ["usha@gmail.com"]
    })

    with pytest.raises(ValueError):
        compare_dataframes(original, cleaned)
