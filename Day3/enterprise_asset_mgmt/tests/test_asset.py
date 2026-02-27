def test_create_asset(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin@test.com",
        "role": "SUPERADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "admin@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.post("/superadmin/assets",
        json={"asset_tag": "LAP001", "asset_type": "Laptop", "brand": "Dell", "model": "XPS 15"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_get_all_assets(client):
    client.post("/auth/register", json={
        "name": "Admin", "email": "admin2@test.com",
        "role": "SUPERADMIN", "password": "pass123"
    })
    login = client.post("/auth/login", json={
        "email": "admin2@test.com", "password": "pass123"
    })
    token = login.json()["access_token"]
    
    response = client.get("/superadmin/assets",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
