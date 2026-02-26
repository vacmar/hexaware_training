from pydantic import BaseModel, ValidationError, field_validator
 
class Employee(BaseModel):
    salary: float
    @field_validator('salary')
    @classmethod
    def check_salary(cls, value):
        if value <= 10000:
            raise ValueError("Salary too low")
        return value
 
#valid input
try:
    emp = Employee(salary=19000)
    print("Valid Employee created")
    print(emp)
except ValidationError as e:
    print("Validation error:", e)
 
#invalid input
try:
    emp = Employee(salary=5000)
    print(emp)
except ValidationError as e:
    print("Validation error:", e)