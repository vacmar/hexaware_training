from sqlalchemy.orm import Session
from app.models.product import Product

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: dict):
        new_product = Product(**product_data)
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_all_products(self):
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int) -> Product:
        return self.db.query(Product).filter(Product.id == product_id).first()

    #def update_product(self, product_id: int, name: str = None, description: str = None, price: float = None, stock: int = None) -> Product:
        product = self.get_product(product_id)
        if not product:
            return None
        if name is not None:
            product.name = name
        if description is not None:
            product.description = description
        if price is not None:
            product.price = price
        if stock is not None:
            product.stock = stock
        self.db.commit()
        self.db.refresh(product)
        return product

    #def delete_product(self, product_id: int) -> bool:
        product = self.get_product(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        return True