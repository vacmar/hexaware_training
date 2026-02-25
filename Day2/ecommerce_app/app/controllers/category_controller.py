from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List 

from app.core.database import get_db
from app.services.category_service import CategoryService
from app.schemas.category_schema import CategoryCreate, CategoryResponse    

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=CategoryResponse)
def create_category(category_data: CategoryCreate, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.create_category(category_data.model_dump())

@router.get("/", response_model=List[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.list_categories()    

@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    service = CategoryService(db)
    return service.get_category(category_id)    