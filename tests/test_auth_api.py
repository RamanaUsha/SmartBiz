
def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == "test@example.com"
    assert data["user_id"] is not None
    assert "hashed_password" not in data


def test_register_duplicate_user(client):
    payload = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }

    first_response = client.post(
        "/auth/register",
        json=payload
    )

    second_response = client.post(
        "/auth/register",
        json=payload
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


def test_register_invalid_email(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "invalid-email",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 422


def test_register_short_password(client):
    response = client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "short"
        }
    )

    assert response.status_code == 422


def test_login_success(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["access_token"]
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword123!"
        }
    )

    assert response.status_code == 401


def test_login_unknown_user(client):
    response = client.post(
        "/auth/login",
        json={
            "email": "unknown@example.com",
            "password": "SecurePass123!"
        }
    )

    assert response.status_code == 401


def test_protected_endpoint_without_token(client):
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_protected_endpoint_with_valid_token(client):
    client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    login_response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "SecurePass123!"
        }
    )

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
    assert "hashed_password" not in response.json()


def test_protected_endpoint_with_invalid_token(client):
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid.token.value"
        }
    )

    assert response.status_code == 401
