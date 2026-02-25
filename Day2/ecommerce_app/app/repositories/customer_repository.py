from sqlalchemy.orm import Session
from app.models.customer import Customer

class CustomerRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_customer(self, customer_data: dict):
        new_customer = Customer(**customer_data)
        self.db.add(new_customer)
        self.db.commit()
        self.db.refresh(new_customer)
        return new_customer

    def get_all_customers(self):
        return self.db.query(Customer).all()

    def get_customer_by_id(self, customer_id: int) -> Customer:
        return self.db.query(Customer).filter(Customer.id == customer_id).first()