def test_create_customer_api(client):
    response = client.post(
        "/customers/",
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
    payload = {
        "name": "Usha",
        "email": "usha@gmail.com"
    }

    first_response = client.post("/customers/", json=payload)

    second_response = client.post(
        "/customers/",
        json={
            "name": "Usha R",
            "email": "USHA@GMAIL.COM"
        }
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_list_customers_api(client):
    client.post(
        "/customers/",
        json={
            "name": "Usha",
            "email": "usha@gmail.com"
        }
    )

    response = client.get("/customers/")

    assert response.status_code == 200

    data = response.json()

    assert data["total_customers"] == 1
    assert data["customers"][0]["name"] == "Usha"


def test_invalid_customer_api(client):
    response = client.post(
        "/customers/",
        json={
            "name": "Usha",
            "email": "invalid-email",
            "phone": "123"
        }
    )

    assert response.status_code == 422