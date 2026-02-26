from pydantic import BaseModel, ValidationError

class Student(BaseModel):
    id: int
    name: str
    age: int
    courses: str
    active: bool