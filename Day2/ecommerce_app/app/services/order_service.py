from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.customer_repository import CustomerRepository 

class OrderService:
    def __init__(self, db: Session):
        self.order_repository = OrderRepository(db)
        self.product_repository = ProductRepository(db)
        self.customer_repository = CustomerRepository(db)

    def create_order(self, order_data: dict):
        # Validate customer
        customer = self.customer_repository.get_customer_by_id(order_data['customer_id'])
        if not customer:
            raise HTTPException(status_code=404, detail="Customer not found")

        # Validate product and stock
        product = self.product_repository.get_product_by_id(order_data['product_id'])
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.stock <=0:
            raise HTTPException(status_code=400, detail="Product out of stock")

        # Reduce stock
        self.order_repository.reduce_stock(order_data['product_id'])
        
        # Create order
        new_order = self.order_repository.create_order(order_data)
        return new_order
    
    def list_orders(self):
        return self.order_repository.get_all_orders()
    
    def get_order(self, order_id: int):
        order = self.order_repository.get_order_by_id(order_id)
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        return order
    