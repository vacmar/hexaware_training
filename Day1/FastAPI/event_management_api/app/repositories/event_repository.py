from core.db import db

class EventRepository:

    def get_all(self):
        return db.events

    def get_by_id(self, event_id: int):
        return next((e for e in db.events if e["id"] == event_id), None)

    def get_by_location(self, location: str):
        return [e for e in db.events if e["location"].lower() == location.lower()]

    def get_by_name(self, name: str):
        return next((e for e in db.events if e["name"].lower() == name.lower()), None)

    def save(self, event_data: dict):
        db.events.append(event_data)
        return event_data