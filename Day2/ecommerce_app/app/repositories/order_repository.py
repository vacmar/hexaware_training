from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.product import Product

class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: dict):
        new_order = Order(**order_data)
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
        return new_order

    def get_all_orders(self):
        return self.db.query(Order).all()

    def get_order_by_id(self, order_id: int) -> Order:
        return self.db.query(Order).filter(Order.id == order_id).first()
    
    def reduce_stock(self, product_id: int):
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock -= 1
            self.db.commit()
            self.db.refresh(product)
            return product
        return None