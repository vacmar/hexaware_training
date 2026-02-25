from pydantic import BaseModel, ConfigDict

class OrderBase(BaseModel):
    customer_id: int
    product_id: int

class OrderCreate(OrderBase):
    pass       

class OrderResponse(OrderBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
        