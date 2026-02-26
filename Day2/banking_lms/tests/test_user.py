from fastapi.testclient import TestClient
from app.main import app


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "john@example.com"
    assert data["name"] == "John Doe"
    assert data["role"] == "customer"


def test_get_user(client):
    # Create a user first
    client.post(
        "/users/",
        json={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "hashed_password": "secure123",
            "role": "loan_officer"
        }
    )
    
    # Get the user
    response = client.get("/users/1")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "jane@example.com"


def test_list_users(client):
    # Create multiple users
    for i in range(3):
        client.post(
            "/users/",
            json={
                "name": f"User {i}",
                "email": f"user{i}@example.com",
                "hashed_password": "secure123",
                "role": "customer"
            }
        )
    
    # List users
    response = client.get("/users/?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3


def test_update_user(client):
    # Create a user
    client.post(
        "/users/",
        json={
            "name": "John",
            "email": "john@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    
    # Update the user
    response = client.put(
        "/users/1",
        json={"name": "John Updated"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Updated"


def test_delete_user(client):
    # Create a user
    client.post(
        "/users/",
        json={
            "name": "John Doe",
            "email": "john@example.com",
            "hashed_password": "secure123",
            "role": "customer"
        }
    )
    
    # Delete the user
    response = client.delete("/users/1")
    assert response.status_code == 204
