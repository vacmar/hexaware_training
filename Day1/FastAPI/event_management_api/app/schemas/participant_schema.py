from pydantic import BaseModel, EmailStr, Field

class ParticipantCreate(BaseModel):
    name: str = Field(..., min_length=2)
    email: EmailStr
    event_id: int

class ParticipantResponse(ParticipantCreate):
    id: int