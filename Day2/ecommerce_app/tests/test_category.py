def test_create_category(client):
    response = client.post("/categories/", json={"name": "Electronics"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Electronics"


def test_list_categories(client):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)