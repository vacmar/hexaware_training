from fastapi import APIRouter, HTTPException
from schemas.participant_schema import ParticipantCreate, ParticipantResponse
from dependencies.service_dependency import participant_service

router = APIRouter()

@router.post("/participants", response_model=ParticipantResponse, status_code=201)
def register_participant(participant: ParticipantCreate):
    try:
        return participant_service.register_participant(participant)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/participants/{participant_id}", response_model=ParticipantResponse)
def get_participant(participant_id: int):
    participant = participant_service.get_participant(participant_id)
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant