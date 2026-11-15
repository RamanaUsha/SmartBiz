
import pandas as pd
import pytest

from app.services.sales_service import (
    validate_sales_data,
    calculate_sales_revenue,
    generate_sales_summary
)


def sample_sales_data():
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "product_name": ["Laptop", "Mouse", "Keyboard"],
        "quantity": [2, 5, 3],
        "unit_price": [50000, 500, 1500]
    })


def test_validate_sales_data():
    dataframe = sample_sales_data()

    assert validate_sales_data(dataframe) is True


def test_calculate_sales_revenue():
    dataframe = sample_sales_data()

    result = calculate_sales_revenue(dataframe)

    assert result["revenue"].tolist() == [
        100000,
        2500,
        4500
    ]


def test_generate_sales_summary():
    dataframe = sample_sales_data()

    result = generate_sales_summary(dataframe)

    assert result["total_orders"] == 3
    assert result["total_quantity_sold"] == 10
    assert result["total_revenue"] == 107000
    assert result["average_order_value"] == pytest.approx(
        35666.67,
        abs=0.01
    )


def test_validate_sales_data_missing_columns():
    dataframe = pd.DataFrame({
        "order_id": [1],
        "product_name": ["Laptop"]
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_sales_data(dataframe)


def test_validate_sales_data_empty_dataframe():
    dataframe = pd.DataFrame(columns=[
        "order_id",
        "product_name",
        "quantity",
        "unit_price"
    ])

    with pytest.raises(ValueError, match="cannot be empty"):
        validate_sales_data(dataframe)


def test_validate_sales_data_invalid_quantity():
    dataframe = sample_sales_data()
    dataframe.loc[0, "quantity"] = 0

    with pytest.raises(ValueError, match="Quantity must be greater than zero"):
        validate_sales_data(dataframe)


def test_validate_sales_data_negative_price():
    dataframe = sample_sales_data()
    dataframe.loc[0, "unit_price"] = -100

    with pytest.raises(ValueError, match="Unit price cannot be negative"):
        validate_sales_data(dataframe)
