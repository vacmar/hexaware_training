from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self, db: Session):
        self.category_repository = CategoryRepository(db)

    def create_category(self, category_data: dict):
        existing_category = self.category_repository.get_category_by_id(category_data.get('id'))
        if existing_category:
            raise HTTPException(status_code=400, detail="Category with this ID already exists")
        return self.category_repository.create_category(category_data)
    
    def list_categories(self):
        return self.category_repository.get_all_categories()
    
    def get_category(self, category_id: int):
        category = self.category_repository.get_category_by_id(category_id)
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        return category