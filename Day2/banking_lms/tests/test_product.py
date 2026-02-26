from fastapi.testclient import TestClient
from app.main import app


def test_create_loan_product(client):
    response = client.post(
        "/loan-products/",
        json={
            "product_name": "Home Loan",
            "interest_rate": 7.5,
            "max_amount": 5000000,
            "tenure_months": 240,
            "description": "Home financing product"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["product_name"] == "Home Loan"
    assert data["interest_rate"] == 7.5


def test_get_loan_product(client):
    # Create a product
    client.post(
        "/loan-products/",
        json={
            "product_name": "Personal Loan",
            "interest_rate": 12.5,
            "max_amount": 500000,
            "tenure_months": 60,
            "description": "Personal loan product"
        }
    )
    
    # Get the product
    response = client.get("/loan-products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["product_name"] == "Personal Loan"


def test_list_loan_products(client):
    # Create multiple products
    for i in range(3):
        client.post(
            "/loan-products/",
            json={
                "product_name": f"Loan Product {i}",
                "interest_rate": 8.5 + i,
                "max_amount": 1000000 + (i * 100000),
                "tenure_months": 120 + (i * 12),
                "description": f"Product {i} description"
            }
        )
    
    # List products
    response = client.get("/loan-products/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_invalid_interest_rate(client):
    response = client.post(
        "/loan-products/",
        json={
            "product_name": "Invalid Loan",
            "interest_rate": 75,  # Invalid: > 50
            "max_amount": 500000,
            "tenure_months": 60,
            "description": "Invalid product"
        }
    )
    assert response.status_code == 400
