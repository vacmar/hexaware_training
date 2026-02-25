from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.services.order_service import OrderService
from app.schemas.order_schema import OrderCreate, OrderResponse

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderResponse)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.create_order(order_data.model_dump())  

@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.list_orders()

@router.get("/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)):
    service = OrderService(db)
    return service.get_order(order_id)