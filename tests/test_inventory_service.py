
import pandas as pd
import pytest

from app.services.inventory_service import (
    validate_inventory_data,
    calculate_inventory_value,
    detect_low_stock,
    generate_inventory_summary
)


def sample_inventory_data():
    return pd.DataFrame({
        "product_id": [101, 102, 103],
        "product_name": ["Laptop", "Mouse", "Keyboard"],
        "quantity": [10, 3, 5],
        "unit_cost": [40000, 300, 1000],
        "reorder_level": [5, 5, 5]
    })


def test_validate_inventory_data():
    dataframe = sample_inventory_data()

    assert validate_inventory_data(dataframe) is True


def test_calculate_inventory_value():
    dataframe = sample_inventory_data()

    result = calculate_inventory_value(dataframe)

    assert result["inventory_value"].tolist() == [
        400000,
        900,
        5000
    ]


def test_detect_low_stock():
    dataframe = sample_inventory_data()

    result = detect_low_stock(dataframe)

    assert len(result) == 2
    assert result["product_name"].tolist() == [
        "Mouse",
        "Keyboard"
    ]


def test_generate_inventory_summary():
    dataframe = sample_inventory_data()

    result = generate_inventory_summary(dataframe)

    assert result["total_products"] == 3
    assert result["total_stock_quantity"] == 18
    assert result["total_inventory_value"] == 405900
    assert result["low_stock_products"] == 2


def test_validate_inventory_missing_columns():
    dataframe = pd.DataFrame({
        "product_id": [101],
        "product_name": ["Laptop"]
    })

    with pytest.raises(ValueError, match="Missing required columns"):
        validate_inventory_data(dataframe)


def test_validate_inventory_empty_dataframe():
    dataframe = pd.DataFrame(columns=[
        "product_id",
        "product_name",
        "quantity",
        "unit_cost",
        "reorder_level"
    ])

    with pytest.raises(ValueError, match="cannot be empty"):
        validate_inventory_data(dataframe)


def test_validate_inventory_negative_quantity():
    dataframe = sample_inventory_data()
    dataframe.loc[0, "quantity"] = -5

    with pytest.raises(ValueError, match="Quantity cannot be negative"):
        validate_inventory_data(dataframe)
