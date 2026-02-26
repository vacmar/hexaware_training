class ParticipantService:

    def __init__(self, participant_repo, event_repo):
        self.participant_repo = participant_repo
        self.event_repo = event_repo
        self.id_counter = 1

    def register_participant(self, participant):

        # Event must exist
        event = self.event_repo.get_by_id(participant.event_id)
        if not event:
            raise ValueError("Event does not exist")

        # Email must be unique
        if self.participant_repo.get_by_email(participant.email):
            raise ValueError("Email already registered")

        # Capacity check
        current_count = self.participant_repo.count_by_event(participant.event_id)
        if current_count >= event["capacity"]:
            raise ValueError("Event capacity exceeded")

        participant_data = participant.model_dump()
        participant_data["id"] = self.id_counter
        self.id_counter += 1

        return self.participant_repo.save(participant_data)

    def get_participant(self, participant_id):
        return self.participant_repo.get_by_id(participant_id)