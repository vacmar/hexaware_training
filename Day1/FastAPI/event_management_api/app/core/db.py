class InMemoryDB:
    def __init__(self):
        self.events = []
        self.participants = []

db = InMemoryDB()