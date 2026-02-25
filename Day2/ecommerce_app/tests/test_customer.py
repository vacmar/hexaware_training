def test_create_customer(client):
    response = client.post("/customers/", json={
        "name": "John Doe", 
        "email": "john.doe@example.com"
        })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    
    