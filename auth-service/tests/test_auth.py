from tests.conftest import get_token


def test_register_customer(client):
    response = client.post(
        "/api/auth/register",
        json={"email": "new@test.com", "full_name": "New User", "password": "pass1234"},
    )
    assert response.status_code == 201
    assert response.json()["role"] == "customer"


def test_register_duplicate_email(client, customer_user):
    response = client.post(
        "/api/auth/register",
        json={"email": "customer@test.com", "full_name": "Dup", "password": "pass1234"},
    )
    assert response.status_code == 400


def test_login_success(client, customer_user):
    response = client.post(
        "/api/auth/login",
        json={"email": "customer@test.com", "password": "password123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password(client, customer_user):
    response = client.post(
        "/api/auth/login",
        json={"email": "customer@test.com", "password": "wrong"},
    )
    assert response.status_code == 401


def test_get_me(client, customer_user):
    token = get_token(client, "customer@test.com")
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["email"] == "customer@test.com"