def get_auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "email": "analytics-test@example.com",
            "password": "SecurePass123!"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "analytics-test@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def sample_payload():
    return {
        "sales": [
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
            },
            {
                "order_id": 4,
                "product_name": "Mouse",
                "quantity": 4,
                "unit_price": 500
            }
        ],
        "inventory": [
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
    }


def test_business_overview_api(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/analytics/business-overview",
        json=sample_payload(),
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == (
        "Business analytics generated successfully"
    )

    overview = data["business_overview"]

    assert overview["total_revenue"] == 109000
    assert overview["total_orders"] == 4
    assert overview["total_quantity_sold"] == 14
    assert overview["total_products"] == 3
    assert overview["total_inventory_value"] == 405900
    assert overview["low_stock_products"] == 2


def test_business_overview_missing_data(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/analytics/business-overview",
        json={"sales": []},
        headers=headers
    )

    assert response.status_code == 400


def test_business_overview_invalid_sales(client):
    headers = get_auth_headers(client)

    payload = sample_payload()
    payload["sales"] = [
        {"order_id": 1}
    ]

    response = client.post(
        "/analytics/business-overview",
        json=payload,
        headers=headers
    )

    assert response.status_code == 400


def test_business_overview_without_token(client):
    response = client.post(
        "/analytics/business-overview",
        json=sample_payload()
    )

    assert response.status_code == 401