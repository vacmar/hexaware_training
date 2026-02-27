def test_create_department(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com",
        "role": "SUPERADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "admin@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.post("/superadmin/departments",
        json={"name": "IT Department"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_get_all_departments(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin2@test.com",
        "role": "SUPERADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "admin2@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.get("/superadmin/departments",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
