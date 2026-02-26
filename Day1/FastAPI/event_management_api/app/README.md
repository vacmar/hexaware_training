# Event Management API

A FastAPI-based REST API for managing events and participant registrations with built-in validation and capacity management.

## Features

- ✅ Create and manage events with location and capacity
- ✅ Register participants with email validation
- ✅ Filter events by location
- ✅ Automatic capacity validation
- ✅ Duplicate prevention (event names & participant emails)
- ✅ Clean layered architecture (Controller → Service → Repository)
- ✅ Interactive API documentation (Swagger UI)

## Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API:**
   - API Base URL: http://127.0.0.1:8000
   - Interactive Docs: http://127.0.0.1:8000/docs
   - Alternative Docs: http://127.0.0.1:8000/redoc

## API Endpoints

### Events

#### Create Event
```http
POST /events
Content-Type: application/json

{
  "name": "Tech Conference 2026",
  "location": "Chennai",
  "capacity": 100
}
```

**Response:** `201 Created`
```json
{
  "name": "Tech Conference 2026",
  "location": "Chennai",
  "capacity": 100,
  "id": 1
}
```

#### List All Events
```http
GET /events
```

#### Filter Events by Location
```http
GET /events?location=Chennai
```

#### Get Event by ID
```http
GET /events/{event_id}
```

### Participants

#### Register Participant
```http
POST /participants
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com",
  "event_id": 1
}
```

**Response:** `201 Created`
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "event_id": 1,
  "id": 1
}
```

#### Get Participant by ID
```http
GET /participants/{participant_id}
```

## Validation Rules

### Events
- **name**: Minimum 3 characters
- **location**: Minimum 2 characters
- **capacity**: Must be greater than 0
- **Unique constraint**: Event names must be unique

### Participants
- **name**: Minimum 2 characters
- **email**: Must be a valid email address
- **Unique constraint**: Email addresses must be unique
- **Capacity check**: Cannot register if event is full

## Project Structure

```
app/
├── main.py                    # FastAPI application entry point
├── controllers/               # API route handlers
│   ├── event_controller.py
│   └── participant_controller.py
├── services/                  # Business logic layer
│   ├── event_service.py
│   └── participant_service.py
├── repositories/              # Data access layer
│   ├── event_repository.py
│   └── participant_repository.py
├── schemas/                   # Pydantic models
│   ├── event_schema.py
│   └── participant_schema.py
├── core/                      # Core utilities
│   └── db.py                  # In-memory database
├── middleware/                # Middleware
│   └── cors_middleware.py
└── dependencies/              # Dependency injection
    └── service_dependency.py
```

## Architecture

The application follows a **clean layered architecture**:

1. **Controllers** - Handle HTTP requests/responses and validation
2. **Services** - Implement business logic and rules
3. **Repositories** - Manage data access and storage
4. **Schemas** - Define data models and validation rules

## Technologies

- **FastAPI** - Modern web framework
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server
- **In-Memory Database** - Simple storage for development

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK` - Successful GET request
- `201 Created` - Successful POST request
- `400 Bad Request` - Validation error
- `404 Not Found` - Resource not found

## Example Usage

### Using cURL

```bash
# Create an event
curl -X POST "http://127.0.0.1:8000/events" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tech Meetup", "location": "Chennai", "capacity": 50}'

# Get all events
curl "http://127.0.0.1:8000/events"

# Filter events by location
curl "http://127.0.0.1:8000/events?location=Chennai"

# Register a participant
curl -X POST "http://127.0.0.1:8000/participants" \
  -H "Content-Type: application/json" \
  -d '{"name": "Jane Smith", "email": "jane@example.com", "event_id": 1}'
```

### Using Python Requests

```python
import requests

# Create an event
response = requests.post(
    "http://127.0.0.1:8000/events",
    json={"name": "Tech Meetup", "location": "Chennai", "capacity": 50}
)
print(response.json())

# Get events in Chennai
response = requests.get("http://127.0.0.1:8000/events?location=Chennai")
print(response.json())
```

## Future Enhancements

- [ ] Database persistence (PostgreSQL/MongoDB)
- [ ] Authentication & authorization
- [ ] Event update/delete endpoints
- [ ] Participant management (update/delete)
- [ ] Advanced search and filtering
- [ ] Pagination for large datasets
- [ ] Event categories and tags
- [ ] Waitlist functionality

## License

This is a sample educational project.