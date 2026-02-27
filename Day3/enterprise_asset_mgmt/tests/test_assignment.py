def test_create_assignment(client):
    client.post("/auth/register", json={
        "name": "IT Admin", "email": "itadmin@test.com",
        "role": "IT_ADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "itadmin@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.post("/itadmin/assignments",
        json={"asset_id": 1, "user_id": 1, "assigned_date": "2024-01-01"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code in [200, 404]

def test_get_assignments(client):
    client.post("/auth/register", json={
        "name": "IT Admin", "email": "itadmin2@test.com",
        "role": "IT_ADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "itadmin2@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.get("/itadmin/assignments",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
