def test_register(client):
    user_data = {
        "name": "John Doe",
        "email": "john@example.com",
        "password": "password123",
        "role": "EMPLOYEE"
    }
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"

def test_login_success(client):
    user_data = {
        "name": "Jane Doe",
        "email": "jane@example.com",
        "password": "password123",
        "role": "EMPLOYEE"
    }
    client.post("/auth/register", json=user_data)
    
    response = client.post("/auth/login", json={
        "email": "jane@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid(client):
    response = client.post("/auth/login", json={
        "email": "wrong@example.com",
        "password": "wrong"
    })
    assert response.status_code == 401
