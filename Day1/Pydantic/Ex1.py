from pydantic import BaseModel, ValidationError, StrictInt
 
class User(BaseModel):
    name: str
    age: StrictInt
    email: str      
 
try:
    user = User(name="Bhuvaneswari", age=30, email="bhuvaneswari@example.com")
    print(user.model_dump())
except ValidationError as e:
    print("Validation error:", e)
 