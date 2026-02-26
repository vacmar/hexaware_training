from pydantic import BaseModel, Field

class EventCreate(BaseModel):
    name: str = Field(..., min_length=3)
    location: str = Field(..., min_length=2)
    capacity: int = Field(..., gt=0)

class EventResponse(EventCreate):
    id: int