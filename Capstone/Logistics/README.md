# Logistics & Shipment Tracking API

A comprehensive RESTful API for a Logistics & Shipment Tracking System built with FastAPI, SQLAlchemy, and PostgreSQL.

## Overview

This system allows:
- **Customers** to create shipments and track deliveries
- **Delivery Agents** to update shipment status
- **Admins** to manage hubs, users, and monitor performance

Similar to platforms like FedEx, Delhivery, or DHL backend systems.

## Technology Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Primary database
- **JWT** - Authentication
- **Docker** - Containerization
- **Redis** - Caching and real-time status updates
- **Pytest** - Testing framework

## Project Structure

```
logistics-api/
├── app/
│   ├── main.py                 # Application entry point
│   ├── core/                   # Core infrastructure
│   │   ├── config.py           # Environment settings
│   │   ├── database.py         # Database connection
│   │   ├── security.py         # JWT & password hashing
│   │   └── dependencies.py     # Dependency injection
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── user.py
│   │   ├── shipment.py
│   │   ├── tracking.py
│   │   └── hub.py
│   ├── schemas/                # Pydantic request/response models
│   ├── repositories/           # Data access layer
│   ├── services/               # Business logic layer
│   ├── api/                    # API routes
│   │   └── routes/
│   ├── middleware/             # CORS, logging, rate limiting
│   ├── exceptions/             # Custom exceptions
│   └── utils/                  # Utility helpers
├── alembic/                    # Database migrations
├── tests/                      # Test suite
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

## Quick Start

### Using Docker (Recommended)

```bash
# Clone and navigate to the project
cd logistics-api

# Start all services
docker-compose up -d

# API will be available at http://localhost:8000
# Swagger docs at http://localhost:8000/docs
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up PostgreSQL and update .env file

# Run the application
uvicorn app.main:app --reload
```

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT token |
| POST | `/auth/token` | Alternative JSON login |

### Shipments
| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| POST | `/shipments` | Create new shipment | Customer |
| GET | `/shipments` | Get user's shipments | Any |
| GET | `/shipments/track/{tracking_number}` | Track shipment | Public |
| GET | `/shipments/{id}` | Get shipment details | Any |
| PUT | `/shipments/{id}` | Update shipment | Customer |
| PUT | `/shipments/{id}/status` | Update status | Agent |
| PUT | `/shipments/{id}/assign-agent` | Assign agent | Admin |
| DELETE | `/shipments/{id}` | Cancel shipment | Customer |

### Tracking
| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| POST | `/tracking/{shipment_id}` | Add tracking update | Agent |
| GET | `/tracking/{shipment_id}` | Get tracking history | Public |
| GET | `/tracking/number/{tracking_number}` | Track by number | Public |

### Hubs
| Method | Endpoint | Description | Role |
|--------|----------|-------------|------|
| GET | `/hubs` | List all hubs | Public |
| GET | `/hubs/{id}` | Get hub details | Public |
| POST | `/hubs` | Create hub | Admin |
| PUT | `/hubs/{id}` | Update hub | Admin |
| DELETE | `/hubs/{id}` | Delete hub | Admin |

### Admin
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/admin/users` | List all users |
| GET | `/admin/users/{id}` | Get user details |
| PUT | `/admin/users/{id}` | Update user |
| DELETE | `/admin/users/{id}` | Delete user |
| GET | `/admin/agents` | List all agents |
| GET | `/admin/reports` | Get statistics report |

## User Roles

- **Customer**: Can create shipments, track deliveries, cancel unshipped orders
- **Agent**: Can update shipment status, add tracking updates
- **Admin**: Full access to all operations including hub and user management

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_auth.py

# Run with coverage
pytest --cov=app tests/
```

## Database Migrations

```bash
# Generate new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one step
alembic downgrade -1
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://...` |
| `SECRET_KEY` | JWT secret key | Required |
| `ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | `30` |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379` |

## Sample API Usage

### Register a Customer
```bash
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "customer@example.com",
    "password": "password123",
    "full_name": "John Doe",
    "role": "customer"
  }'
```

### Login
```bash
curl -X POST "http://localhost:8000/auth/login" \
  -d "username=customer@example.com&password=password123"
```

### Create Shipment
```bash
curl -X POST "http://localhost:8000/shipments" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "source_address": "Chennai, Tamil Nadu",
    "destination_address": "Bangalore, Karnataka"
  }'
```

### Track Shipment
```bash
curl "http://localhost:8000/shipments/track/TRK1234567890"
```

## License

MIT License
