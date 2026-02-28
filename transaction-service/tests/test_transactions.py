import uuid
from app.models.account import Account, AccountStatus


def create_test_accounts(db, user_id):
    acc1 = Account(
        id=uuid.uuid4(),
        user_id=uuid.UUID(user_id),
        account_number="1111111111",
        balance=5000.0,
        status=AccountStatus.active,
    )
    acc2 = Account(
        id=uuid.uuid4(),
        user_id=uuid.uuid4(),
        account_number="2222222222",
        balance=0.0,
        status=AccountStatus.active,
    )
    db.add(acc1)
    db.add(acc2)
    db.commit()
    return acc1, acc2


def test_deposit(client, customer_token, db):
    from tests.conftest import TEST_USER_ID
    acc1, _ = create_test_accounts(db, TEST_USER_ID)
    response = client.post(
        "/api/transactions/deposit",
        json={"account_id": str(acc1.id), "amount": 1000},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 201
    assert response.json()["amount"] == 1000
    assert response.json()["type"] == "deposit"


def test_get_transactions(client, customer_token, db):
    response = client.get(
        "/api/transactions",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)