def test_create_product(client):
    #first create a category
    client.post("/categories/", json={"name": "Electronics"})
    response = client.post("/products/", json={
        "name": "Laptop", 
        "description": "A high-performance laptop", 
        "price": 999.99, 
        "stock": 10,
        "category_id": 1
        })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Laptop"
    assert data["stock"] == 10
    
def test_product_validation(client):
    response = client.post("/products/", json={
        "name": "Invalid Product", 
        "description": "This product has invalid price and stock", 
        "price": -10, 
        "stock": 5,
        "category_id": 1
        })
    assert response.status_code == 422
    data = response.json()
    assert data["detail"][0]["msg"] == "Input should be greater than 0"