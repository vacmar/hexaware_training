from sqlalchemy.orm import Session
from app.models.category import Category

class CategoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_category(self, category_data: dict):
        new_category = Category(**category_data)
        self.db.add(new_category)
        self.db.commit()
        self.db.refresh(new_category)
        return new_category

    def get_all_categories(self):
        return self.db.query(Category).all()

    def get_category_by_id(self, category_id: int) -> Category:
        return self.db.query(Category).filter(Category.id == category_id).first()