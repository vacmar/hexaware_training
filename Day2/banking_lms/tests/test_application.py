from fastapi.testclient import TestClient
from app.main import app


def test_create_loan_application(client):
    # Create a user
    client.post(
        "/users/",
        json={
            "name": "Customer",
            "email": "customer@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    
    # Create a loan product
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
    
    # Create loan application
    response = client.post(
        "/loan-applications/",
        json={
            "user_id": 1,
            "product_id": 1,
            "requested_amount": 2000000
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["user_id"] == 1
    assert data["requested_amount"] == 2000000
    assert data["status"] == "pending"


def test_application_exceeds_max_amount(client):
    # Create a user
    client.post(
        "/users/",
        json={
            "name": "Customer",
            "email": "customer@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    
    # Create a loan product
    client.post(
        "/loan-products/",
        json={
            "product_name": "Personal Loan",
            "interest_rate": 12.5,
            "max_amount": 500000,  # Max amount
            "tenure_months": 60,
            "description": "Personal loan"
        }
    )
    
    # Try to create application exceeding max amount
    response = client.post(
        "/loan-applications/",
        json={
            "user_id": 1,
            "product_id": 1,
            "requested_amount": 1000000  # Exceeds max
        }
    )
    assert response.status_code == 400


def test_list_loan_applications(client):
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
    
    # Create multiple applications
    for i in range(2):
        client.post(
            "/loan-applications/",
            json={
                "user_id": 1,
                "product_id": 1,
                "requested_amount": 1000000 + (i * 100000)
            }
        )
    
    # List applications
    response = client.get("/loan-applications/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_update_application_status(client):
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
    
    # Update status to approved
    response = client.put(
        "/loan-applications/1/status",
        json={
            "status": "approved",
            "approved_amount": 2000000
        },
        params={"processed_by": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["approved_amount"] == 2000000
