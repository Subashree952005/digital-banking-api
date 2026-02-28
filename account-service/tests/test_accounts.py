def test_create_account(client, customer_token, db):
    response = client.post(
        "/api/accounts",
        json={"initial_deposit": 5000},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 201
    assert response.json()["balance"] == 5000
    assert response.json()["status"] == "active"


def test_create_account_zero(client, customer_token, db):
    response = client.post(
        "/api/accounts",
        json={"initial_deposit": 0},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 201
    assert response.json()["balance"] == 0


def test_list_accounts(client, customer_token, db):
    client.post("/api/accounts", json={"initial_deposit": 100},
        headers={"Authorization": f"Bearer {customer_token}"})
    client.post("/api/accounts", json={"initial_deposit": 200},
        headers={"Authorization": f"Bearer {customer_token}"})
    response = client.get("/api/accounts",
        headers={"Authorization": f"Bearer {customer_token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_freeze_account(client, customer_token, admin_token, db):
    acc = client.post("/api/accounts", json={"initial_deposit": 100},
        headers={"Authorization": f"Bearer {customer_token}"}).json()
    response = client.put(
        f"/api/accounts/{acc['id']}/freeze",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "frozen"