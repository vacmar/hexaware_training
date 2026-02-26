class EventService:

    def __init__(self, event_repo):
        self.event_repo = event_repo
        self.id_counter = 1

    def create_event(self, event):
        # Prevent duplicate event names
        if self.event_repo.get_by_name(event.name):
            raise ValueError("Event name already exists")

        event_data = event.model_dump()
        event_data["id"] = self.id_counter
        self.id_counter += 1

        return self.event_repo.save(event_data)

    def list_events(self, location=None):
        if location:
            return self.event_repo.get_by_location(location)
        return self.event_repo.get_all()

    def get_event(self, event_id):
        return self.event_repo.get_by_id(event_id)