from tests.conftest import get_token


def test_apply_loan(client, customer_user):
    token = get_token(client, "customer@test.com")
    response = client.post(
        "/api/loans/apply",
        json={"amount": 500000, "duration_months": 24, "purpose": "Home renovation"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "pending"
    assert data["amount"] == 500000


def test_officer_approve_loan(client, customer_user, officer_user):
    customer_token = get_token(client, "customer@test.com")
    officer_token = get_token(client, "officer@test.com")
    loan = client.post(
        "/api/loans/apply",
        json={"amount": 100000, "duration_months": 12},
        headers={"Authorization": f"Bearer {customer_token}"},
    ).json()
    response = client.put(
        f"/api/loans/{loan['id']}/approve",
        json={"officer_note": "Approved"},
        headers={"Authorization": f"Bearer {officer_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "approved"


def test_officer_reject_loan(client, customer_user, officer_user):
    customer_token = get_token(client, "customer@test.com")
    officer_token = get_token(client, "officer@test.com")
    loan = client.post(
        "/api/loans/apply",
        json={"amount": 100000, "duration_months": 12},
        headers={"Authorization": f"Bearer {customer_token}"},
    ).json()
    response = client.put(
        f"/api/loans/{loan['id']}/reject",
        json={"officer_note": "Rejected"},
        headers={"Authorization": f"Bearer {officer_token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


def test_customer_cannot_approve(client, customer_user):
    token = get_token(client, "customer@test.com")
    loan = client.post(
        "/api/loans/apply",
        json={"amount": 50000},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    response = client.put(
        f"/api/loans/{loan['id']}/approve",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403


def test_emi_calculation(client, customer_user):
    token = get_token(client, "customer@test.com")
    loan = client.post(
        "/api/loans/apply",
        json={"amount": 100000, "duration_months": 12},
        headers={"Authorization": f"Bearer {token}"},
    ).json()
    response = client.get(
        f"/api/loans/{loan['id']}/emi",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["monthly_emi"] > 0
    assert data["total_payable"] > data["principal"]


def test_admin_reports(client, admin_user):
    token = get_token(client, "admin@test.com")
    response = client.get(
        "/api/admin/reports",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "total_accounts" in data
    assert "total_loans" in data
    assert "total_transactions_today" in data