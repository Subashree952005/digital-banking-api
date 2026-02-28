from tests.conftest import get_token
from app.models.user import User, UserRole
from app.core.security import hash_password


def create_second_user(db):
    user = User(
        email="user2@test.com",
        full_name="User Two",
        password_hash=hash_password("password123"),
        role=UserRole.customer,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def test_transfer_money(client, customer_user, db):
    create_second_user(db)
    token1 = get_token(client, "customer@test.com")
    token2 = get_token(client, "user2@test.com")
    acc1 = client.post("/api/accounts",
        json={"initial_deposit": 5000},
        headers={"Authorization": f"Bearer {token1}"}).json()
    acc2 = client.post("/api/accounts",
        json={"initial_deposit": 0},
        headers={"Authorization": f"Bearer {token2}"}).json()
    response = client.post(
        "/api/transactions/transfer",
        json={"to_account": acc2["account_number"], "amount": 1000},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 1000
    assert response.json()["type"] == "transfer"


def test_transfer_insufficient_funds(client, customer_user, db):
    create_second_user(db)
    token1 = get_token(client, "customer@test.com")
    token2 = get_token(client, "user2@test.com")
    client.post("/api/accounts",
        json={"initial_deposit": 100},
        headers={"Authorization": f"Bearer {token1}"})
    acc2 = client.post("/api/accounts",
        json={"initial_deposit": 0},
        headers={"Authorization": f"Bearer {token2}"}).json()
    response = client.post(
        "/api/transactions/transfer",
        json={"to_account": acc2["account_number"], "amount": 5000},
        headers={"Authorization": f"Bearer {token1}"},
    )
    assert response.status_code == 400


def test_deposit(client, customer_user):
    token = get_token(client, "customer@test.com")
    acc = client.post("/api/accounts",
        json={"initial_deposit": 0},
        headers={"Authorization": f"Bearer {token}"}).json()
    response = client.post(
        "/api/transactions/deposit",
        json={"account_id": acc["id"], "amount": 2000},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 2000


def test_withdraw(client, customer_user):
    token = get_token(client, "customer@test.com")
    acc = client.post("/api/accounts",
        json={"initial_deposit": 1000},
        headers={"Authorization": f"Bearer {token}"}).json()
    response = client.post(
        "/api/transactions/withdraw",
        json={"account_id": acc["id"], "amount": 500},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 500


def test_get_transactions(client, customer_user):
    token = get_token(client, "customer@test.com")
    acc = client.post("/api/accounts",
        json={"initial_deposit": 1000},
        headers={"Authorization": f"Bearer {token}"}).json()
    client.post("/api/transactions/withdraw",
        json={"account_id": acc["id"], "amount": 100},
        headers={"Authorization": f"Bearer {token}"})
    response = client.get(
        "/api/transactions",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert len(response.json()) >= 1