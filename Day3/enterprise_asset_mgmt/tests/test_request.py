def test_create_request(client):
    client.post("/auth/register", json={
        "name": "Employee", "email": "employee@test.com",
        "role": "EMPLOYEE", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "employee@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.post("/employee/requests",
        json={"asset_type": "Laptop", "reason": "Need for work"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_get_user_requests(client):
    client.post("/auth/register", json={
        "name": "Employee", "email": "employee2@test.com",
        "role": "EMPLOYEE", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "employee2@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.get("/employee/requests",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
