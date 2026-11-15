def get_auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "email": "inventory-test@example.com",
            "password": "SecurePass123!"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "inventory-test@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_analyze_inventory_success(client):
    headers = get_auth_headers(client)

    records = [
        {
            "product_id": 101,
            "product_name": "Laptop",
            "quantity": 10,
            "unit_cost": 40000,
            "reorder_level": 5
        },
        {
            "product_id": 102,
            "product_name": "Mouse",
            "quantity": 3,
            "unit_cost": 300,
            "reorder_level": 5
        },
        {
            "product_id": 103,
            "product_name": "Keyboard",
            "quantity": 5,
            "unit_cost": 1000,
            "reorder_level": 5
        }
    ]

    response = client.post(
        "/inventory/analyze",
        json=records,
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Inventory data analyzed successfully"

    assert data["summary"]["total_products"] == 3
    assert data["summary"]["total_stock_quantity"] == 18
    assert data["summary"]["total_inventory_value"] == 405900
    assert data["summary"]["low_stock_products"] == 2

    assert [
        product["product_name"]
        for product in data["low_stock_products"]
    ] == ["Mouse", "Keyboard"]


def test_analyze_inventory_missing_columns(client):
    headers = get_auth_headers(client)

    records = [
        {
            "product_id": 101,
            "product_name": "Laptop"
        }
    ]

    response = client.post(
        "/inventory/analyze",
        json=records,
        headers=headers
    )

    assert response.status_code == 400
    assert "Missing required columns" in response.json()["detail"]


def test_analyze_inventory_empty_records(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/inventory/analyze",
        json=[],
        headers=headers
    )

    assert response.status_code == 400


def test_analyze_inventory_without_token(client):
    response = client.post(
        "/inventory/analyze",
        json=[
            {
                "product_id": 101,
                "product_name": "Laptop",
                "quantity": 10,
                "unit_cost": 40000,
                "reorder_level": 5
            }
        ]
    )

    assert response.status_code == 401