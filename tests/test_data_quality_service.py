
import pandas as pd
import pytest

from app.services.data_quality_service import (
    generate_data_overview,
    generate_missing_value_report,
    generate_duplicate_report,
    generate_invalid_email_report,
    calculate_data_quality_score
)


@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "name": ["Usha", "Ravi", "Usha", "Anu"],
        "email": [
            "usha@gmail.com",
            "ravi.gmail.com",
            "usha@gmail.com",
            None
        ],
        "city": [
            "Chittoor",
            None,
            "Chittoor",
            "Bangalore"
        ]
    })


def test_generate_data_overview(sample_dataframe):
    result = generate_data_overview(sample_dataframe)

    assert result["total_rows"] == 4
    assert result["total_columns"] == 3
    assert result["column_names"] == ["name", "email", "city"]


def test_generate_missing_value_report(sample_dataframe):
    result = generate_missing_value_report(sample_dataframe)

    assert result["missing_values"]["email"] == 1
    assert result["missing_values"]["city"] == 1
    assert result["total_missing_values"] == 2


def test_generate_duplicate_report(sample_dataframe):
    result = generate_duplicate_report(
        sample_dataframe,
        ["email"]
    )

    assert result["duplicate_count"] == 1
    assert len(result["duplicate_rows"]) == 1


def test_generate_invalid_email_report(sample_dataframe):
    result = generate_invalid_email_report(
        sample_dataframe,
        "email"
    )

    assert result["invalid_email_count"] == 1
    assert result["invalid_email_rows"][0]["name"] == "Ravi"


def test_calculate_data_quality_score(sample_dataframe):
    score = calculate_data_quality_score(
        sample_dataframe,
        ["email"],
        "email"
    )

    assert score == 78.33


def test_calculate_score_for_empty_dataframe():
    dataframe = pd.DataFrame()

    with pytest.raises(ValueError):
        calculate_data_quality_score(
            dataframe,
            ["email"],
            "email"
        )
