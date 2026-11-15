import pytest


def test_analyze_sales_success(client):
    records = [
        {
            "order_id": 1,
            "product_name": "Laptop",
            "quantity": 2,
            "unit_price": 50000
        },
        {
            "order_id": 2,
            "product_name": "Mouse",
            "quantity": 5,
            "unit_price": 500
        },
        {
            "order_id": 3,
            "product_name": "Keyboard",
            "quantity": 3,
            "unit_price": 1500
        }
    ]

    response = client.post(
        "/sales/analyze",
        json=records
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Sales data analyzed successfully"
    assert data["summary"]["total_orders"] == 3
    assert data["summary"]["total_quantity_sold"] == 10
    assert data["summary"]["total_revenue"] == 107000

    assert data["summary"]["average_order_value"] == pytest.approx(
        35666.67,
        abs=0.01
    )

    assert [
        record["revenue"]
        for record in data["sales_records"]
    ] == [100000, 2500, 4500]


def test_analyze_sales_missing_columns(client):
    records = [
        {
            "order_id": 1,
            "product_name": "Laptop"
        }
    ]

    response = client.post(
        "/sales/analyze",
        json=records
    )

    assert response.status_code == 400
    assert "Missing required columns" in response.json()["detail"]


def test_analyze_sales_empty_records(client):
    response = client.post(
        "/sales/analyze",
        json=[]
    )

    assert response.status_code == 400