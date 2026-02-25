from pydantic import BaseModel

class CourseCreate(BaseModel):
    title: str
    duration: int

class CourseResponse(BaseModel):
    id: int
    title: str
    duration: int

    class Config:
        from_attributes = True