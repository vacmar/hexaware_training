from pydantic import BaseModel, ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass    

class CategoryResponse(CategoryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)