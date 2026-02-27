def test_create_user(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com",
        "role": "SUPERADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "admin@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.post("/superadmin/users",
        json={"name": "User1", "email": "user1@test.com", "role": "EMPLOYEE", "password": "pass123"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_get_all_users(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin2@test.com",
        "role": "SUPERADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "admin2@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.get("/superadmin/users",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
