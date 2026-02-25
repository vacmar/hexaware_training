from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductResponse

router = APIRouter(prefix="/products", tags=["Products"])
#service = ProductService()

@router.post("/", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.create_product(product_data.model_dump())

@router.get("/", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.list_products()

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    service = ProductService(db)
    return service.get_product(product_id)  