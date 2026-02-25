from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.customer_repository import CustomerRepository

class CustomerService:
    def __init__(self, db: Session):
        self.customer_repository = CustomerRepository(db)

    def create_customer(self, customer_data: dict):
        existing_customer = self.customer_repository.get_customer_by_id(customer_data.get('id'))
        if existing_customer:
            raise HTTPException(status_code=400, detail="Customer with this ID already exists")
        return self.customer_repository.create_customer(customer_data)
    
    def list_customers(self):
        return self.customer_repository.get_all_customers()
    
    def get_customer(self, customer_id: int):
        customer = self.customer_repository.get_customer_by_id(customer_id)
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")
        return customer