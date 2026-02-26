from repositories.event_repository import EventRepository
from repositories.participant_repository import ParticipantRepository
from services.event_service import EventService
from services.participant_service import ParticipantService

event_repo = EventRepository()
participant_repo = ParticipantRepository()

event_service = EventService(event_repo)
participant_service = ParticipantService(participant_repo, event_repo)