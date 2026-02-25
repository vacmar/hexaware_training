from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

#used to creating a product
class ProductBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    description: Optional[str] = Field(None)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: int
    
class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    stock: Optional[int]
    category_id: Optional[int]
      
#used when return a product data
class ProductResponse(ProductBase):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock: int
    model_config = ConfigDict(from_attributes=True)