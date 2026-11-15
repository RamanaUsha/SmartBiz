import pandas as pd

from app.services.analytics_service import (
    generate_business_analytics
)


def sample_sales_data():
    return pd.DataFrame({
        "order_id": [1, 2, 3, 4],
        "product_name": [
            "Laptop",
            "Mouse",
            "Keyboard",
            "Mouse"
        ],
        "quantity": [2, 5, 3, 4],
        "unit_price": [50000, 500, 1500, 500]
    })


def sample_inventory_data():
    return pd.DataFrame({
        "product_id": [101, 102, 103],
        "product_name": [
            "Laptop",
            "Mouse",
            "Keyboard"
        ],
        "quantity": [10, 3, 5],
        "unit_cost": [40000, 300, 1000],
        "reorder_level": [5, 5, 5]
    })


def test_generate_business_analytics():
    sales = sample_sales_data()
    inventory = sample_inventory_data()

    result = generate_business_analytics(
        sales,
        inventory
    )

    overview = result["business_overview"]

    assert overview["total_revenue"] == 109000
    assert overview["total_orders"] == 4
    assert overview["total_quantity_sold"] == 14
    assert overview["total_products"] == 3
    assert overview["total_inventory_value"] == 405900
    assert overview["low_stock_products"] == 2


def test_top_selling_products():
    result = generate_business_analytics(
        sample_sales_data(),
        sample_inventory_data()
    )

    products = result["top_selling_products"]

    assert products[0]["product_name"] == "Mouse"
    assert products[0]["quantity_sold"] == 9
    assert products[0]["total_revenue"] == 4500


def test_low_stock_alerts():
    result = generate_business_analytics(
        sample_sales_data(),
        sample_inventory_data()
    )

    alerts = result["low_stock_alerts"]

    assert len(alerts) == 2

    assert [
        product["product_name"]
        for product in alerts
    ] == ["Mouse", "Keyboard"]