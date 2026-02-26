from fastapi.testclient import TestClient
from app.main import app


def test_create_repayment(client):
    # Setup: Create user, product, and approved application
    client.post(
        "/users/",
        json={
            "name": "Customer",
            "email": "customer@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    
    client.post(
        "/loan-products/",
        json={
            "product_name": "Home Loan",
            "interest_rate": 7.5,
            "max_amount": 5000000,
            "tenure_months": 240,
            "description": "Home financing"
        }
    )
    
    client.post(
        "/loan-applications/",
        json={
            "user_id": 1,
            "product_id": 1,
            "requested_amount": 2000000
        }
    )
    
    # Approve the application
    client.put(
        "/loan-applications/1/status",
        json={
            "status": "approved",
            "approved_amount": 2000000
        },
        params={"processed_by": 1}
    )
    
    # Disburse the application
    client.put(
        "/loan-applications/1/status",
        json={"status": "disbursed"},
        params={"processed_by": 1}
    )
    
    # Create repayment
    response = client.post(
        "/repayments/",
        json={
            "loan_application_id": 1,
            "amount_paid": 100000,
            "payment_status": "completed"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["amount_paid"] == 100000
    assert data["payment_status"] == "completed"


def test_get_application_repayments(client):
    # Setup
    client.post(
        "/users/",
        json={
            "name": "Customer",
            "email": "customer@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    
    client.post(
        "/loan-products/",
        json={
            "product_name": "Home Loan",
            "interest_rate": 7.5,
            "max_amount": 5000000,
            "tenure_months": 240,
            "description": "Home financing"
        }
    )
    
    client.post(
        "/loan-applications/",
        json={
            "user_id": 1,
            "product_id": 1,
            "requested_amount": 2000000
        }
    )
    
    # Approve and disburse
    client.put(
        "/loan-applications/1/status",
        json={
            "status": "approved",
            "approved_amount": 2000000
        },
        params={"processed_by": 1}
    )
    
    client.put(
        "/loan-applications/1/status",
        json={"status": "disbursed"},
        params={"processed_by": 1}
    )
    
    # Create repayments
    for i in range(2):
        client.post(
            "/repayments/",
            json={
                "loan_application_id": 1,
                "amount_paid": 100000 + (i * 10000),
                "payment_status": "completed"
            }
        )
    
    # Get repayments
    response = client.get("/repayments/application/1")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
