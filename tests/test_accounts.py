from tests.conftest import get_token


def test_create_account(client, customer_user):
    token = get_token(client, "customer@test.com")
    response = client.post(
        "/api/accounts",
        json={"initial_deposit": 5000},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["balance"] == 5000
    assert data["status"] == "active"
    assert len(data["account_number"]) == 10


def test_create_account_zero_deposit(client, customer_user):
    token = get_token(client, "customer@test.com")
    response = client.post(
        "/api/accounts",
        json={"initial_deposit": 0},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["balance"] == 0


def test_get_account(client, customer_user):
    token = get_token(client, "customer@test.com")
    acc = client.post(
        "/api/accounts",
        json={"initial_deposit": 1000},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    response = client.get(
        f"/api/accounts/{acc['id']}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["balance"] == 1000


def test_list_accounts(client, customer_user):
    token = get_token(client, "customer@test.com")
    client.post("/api/accounts", json={"initial_deposit": 100},
        headers={"Authorization": f"Bearer {token}"})
    client.post("/api/accounts", json={"initial_deposit": 200},
        headers={"Authorization": f"Bearer {token}"})
    response = client.get(
        "/api/accounts",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_freeze_account_admin_only(client, customer_user, admin_user):
    customer_token = get_token(client, "customer@test.com")
    admin_token = get_token(client, "admin@test.com")
    acc = client.post(
        "/api/accounts",
        json={"initial_deposit": 100},
        headers={"Authorization": f"Bearer {customer_token}"},
    ).json()
    r = client.put(
        f"/api/accounts/{acc['id']}/freeze",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert r.status_code == 403
    r = client.put(
        f"/api/accounts/{acc['id']}/freeze",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert r.status_code == 200
    assert r.json()["status"] == "frozen"