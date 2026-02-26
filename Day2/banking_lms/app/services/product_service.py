from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.product_repository import ProductRepository


class ProductService:
    def __init__(self, db: Session):
        self.product_repository = ProductRepository(db)

    def create_product(self, product_data: dict):
        # Business Logic Validation
        if product_data['interest_rate'] < 0 or product_data['interest_rate'] > 50:
            raise HTTPException(status_code=400, detail="Interest rate must be between 0 and 50")
        if product_data['max_amount'] <= 0:
            raise HTTPException(status_code=400, detail="Max amount must be greater than zero")
        if product_data['tenure_months'] <= 0:
            raise HTTPException(status_code=400, detail="Tenure months must be greater than zero")
        
        return self.product_repository.create_product(product_data)
    
    def list_products(self, skip: int = 0, limit: int = 10):
        if skip < 0 or limit < 1:
            raise HTTPException(status_code=400, detail="Invalid pagination parameters")
        return self.product_repository.get_all_products(skip, limit)
    
    def get_product(self, product_id: int):
        product = self.product_repository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Loan product not found")
        return product
    
    def update_product(self, product_id: int, product_data: dict):
        product = self.get_product(product_id)  # Validate product exists
        
        # Validate interest_rate if being updated
        if 'interest_rate' in product_data and product_data['interest_rate']:
            if product_data['interest_rate'] < 0 or product_data['interest_rate'] > 50:
                raise HTTPException(status_code=400, detail="Interest rate must be between 0 and 50")
        
        return self.product_repository.update_product(product_id, 
                                                     {k: v for k, v in product_data.items() if v is not None})
    
    def delete_product(self, product_id: int):
        product = self.get_product(product_id)  # Validate product exists
        return self.product_repository.delete_product(product_id)
