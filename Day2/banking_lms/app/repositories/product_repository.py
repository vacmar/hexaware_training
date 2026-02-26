from sqlalchemy.orm import Session
from app.models.loan_product import LoanProduct


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: dict):
        new_product = LoanProduct(**product_data)
        self.db.add(new_product)
        self.db.commit()
        self.db.refresh(new_product)
        return new_product

    def get_all_products(self, skip: int = 0, limit: int = 10):
        return self.db.query(LoanProduct).offset(skip).limit(limit).all()

    def get_product_by_id(self, product_id: int) -> LoanProduct:
        return self.db.query(LoanProduct).filter(LoanProduct.id == product_id).first()

    def update_product(self, product_id: int, product_data: dict) -> LoanProduct:
        product = self.get_product_by_id(product_id)
        if not product:
            return None
        for key, value in product_data.items():
            if value is not None:
                setattr(product, key, value)
        self.db.commit()
        self.db.refresh(product)
        return product

    def delete_product(self, product_id: int) -> bool:
        product = self.get_product_by_id(product_id)
        if not product:
            return False
        self.db.delete(product)
        self.db.commit()
        return True

    def count_products(self) -> int:
        return self.db.query(LoanProduct).count()
