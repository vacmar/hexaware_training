from pydantic import BaseModel, ValidationError, Field

class Product(BaseModel):
    name: str = Field(..., description="Name of the product")
    price: float = Field(..., gt=0) #greater than 0
    stock: int = Field(..., ge=0) #greater than or equal to 0

try:
    product = Product(name="Laptop", price=999.99, stock=10)
    print(product.model_dump())
except ValidationError as e:
    print("Validation error:", e)

try:
    invalid_product = Product(name="Smartphone", price=-499.99, stock=-5)
    print(invalid_product.model_dump())
except ValidationError as e:
    print("Validation error:", e)
