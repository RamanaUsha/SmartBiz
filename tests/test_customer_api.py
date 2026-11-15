
def get_auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "email": "customer-test@example.com",
            "password": "SecurePass123!"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "customer-test@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login_response.json()["access_token"]

    return {
        "Authorization": f"Bearer {token}"
    }


def test_create_customer_api(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/customers/",
        headers=headers,
        json={
            "name": "Usha",
            "email": "usha@gmail.com",
            "phone": "9876543210",
            "city": "Chittoor"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["customer"]["name"] == "Usha"
    assert data["customer"]["email"] == "usha@gmail.com"
    assert data["customer"]["customer_id"] is not None


def test_duplicate_customer_api(client):
    headers = get_auth_headers(client)

    payload = {
        "name": "Usha",
        "email": "usha@gmail.com"
    }

    first_response = client.post(
        "/customers/",
        headers=headers,
        json=payload
    )

    second_response = client.post(
        "/customers/",
        headers=headers,
        json={
            "name": "Usha R",
            "email": "USHA@GMAIL.COM"
        }
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_list_customers_api(client):
    headers = get_auth_headers(client)

    client.post(
        "/customers/",
        headers=headers,
        json={
            "name": "Usha",
            "email": "usha@gmail.com"
        }
    )

    response = client.get(
        "/customers/",
        headers=headers
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_customers"] == 1
    assert data["customers"][0]["name"] == "Usha"


def test_invalid_customer_api(client):
    headers = get_auth_headers(client)

    response = client.post(
        "/customers/",
        headers=headers,
        json={
            "name": "Usha",
            "email": "invalid-email",
            "phone": "123"
        }
    )

    assert response.status_code == 422


def test_create_customer_without_token(client):
    response = client.post(
        "/customers/",
        json={
            "name": "Usha",
            "email": "usha@gmail.com"
        }
    )

    assert response.status_code == 401


def test_list_customers_without_token(client):
    response = client.get("/customers/")

    assert response.status_code == 401
