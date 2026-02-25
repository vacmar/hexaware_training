def test_create_order(client):
    # First, create a category and a product
    client.post("/categories/", json={"name": "Electronics"})
    client.post("/products/", json={
        "name": "Laptop", 
        "description": "A high-performance laptop", 
        "price": 999.99, 
        "stock": 10,
        "category_id": 1
        })
    # Then, create a customer
    client.post("/customers/", json={
        "name": "John Doe", "email": "john.doe@example.com"})
    
    #create order
    response = client.post("/orders/", json={
        "customer_id": 1,
        "product_id": 1,
    })
    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == 1