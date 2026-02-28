def test_apply_loan(client, customer_token):
    response = client.post(
        "/api/loans/apply",
        json={"amount": 500000, "duration_months": 24, "purpose": "Home renovation"},
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 201
    assert response.json()["status"] == "pending"
    assert response.json()["amount"] == 500000


def test_officer_approve_loan(client, customer_token, officer_token):
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


def test_officer_reject_loan(client, customer_token, officer_token):
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


def test_customer_cannot_approve(client, customer_token):
    loan = client.post(
        "/api/loans/apply",
        json={"amount": 50000},
        headers={"Authorization": f"Bearer {customer_token}"},
    ).json()
    response = client.put(
        f"/api/loans/{loan['id']}/approve",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 403


def test_emi_calculation(client, customer_token):
    loan = client.post(
        "/api/loans/apply",
        json={"amount": 100000, "duration_months": 12},
        headers={"Authorization": f"Bearer {customer_token}"},
    ).json()
    response = client.get(
        f"/api/loans/{loan['id']}/emi",
        headers={"Authorization": f"Bearer {customer_token}"},
    )
    assert response.status_code == 200
    assert response.json()["monthly_emi"] > 0
    assert response.json()["total_payable"] > response.json()["principal"]


def test_list_loans_customer(client, customer_token):
    client.post("/api/loans/apply",
        json={"amount": 50000, "duration_months": 6},
        headers={"Authorization": f"Bearer {customer_token}"})
    response = client.get("/api/loans",
        headers={"Authorization": f"Bearer {customer_token}"})
    assert response.status_code == 200
    assert len(response.json()) >= 1