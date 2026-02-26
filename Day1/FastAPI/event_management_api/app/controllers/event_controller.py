from fastapi import APIRouter, HTTPException
from schemas.event_schema import EventCreate, EventResponse
from dependencies.service_dependency import event_service

router = APIRouter()

@router.post("/events", response_model=EventResponse, status_code=201)
def create_event(event: EventCreate):
    try:
        return event_service.create_event(event)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/events", response_model=list[EventResponse])
def list_events(location: str | None = None):
    return event_service.list_events(location)


@router.get("/events/{event_id}", response_model=EventResponse)
def get_event(event_id: int):
    event = event_service.get_event(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event