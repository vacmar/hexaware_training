from core.db import db

class ParticipantRepository:

    def save(self, participant_data: dict):
        db.participants.append(participant_data)
        return participant_data

    def get_by_id(self, participant_id: int):
        return next((p for p in db.participants if p["id"] == participant_id), None)

    def get_by_email(self, email: str):
        return next((p for p in db.participants if p["email"] == email), None)

    def count_by_event(self, event_id: int):
        return len([p for p in db.participants if p["event_id"] == event_id])