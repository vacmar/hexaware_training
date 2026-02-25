from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.product_repository import ProductRepository

class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def create_product(self, product_data: dict):
        if product_data['price'] <= 0:
            raise HTTPException(status_code=400, detail="Price must be greater than zero")
        if product_data['stock'] < 0:
            raise HTTPException(status_code=400, detail="Stock cannot be negative")
        return self.product_repository.create_product(product_data)
    
    def list_products(self):
        return self.product_repository.get_all_products()
    
    def get_product(self, product_id: int):
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    