# Logistics Microservices Architecture

This directory contains the microservices architecture for the Logistics & Shipment Tracking API.

## Architecture Overview

```
                    ┌─────────────────┐
                    │   API Gateway   │
                    │   (Port 8000)   │
                    └────────┬────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        ▼                    ▼                    ▼
┌───────────────┐  ┌─────────────────┐  ┌─────────────────┐
│ Auth Service  │  │  Hub Service    │  │Shipment Service │
│  (Port 8001)  │  │  (Port 8002)    │  │  (Port 8003)    │
└───────────────┘  └─────────────────┘  └─────────────────┘
        │                    │                    │
        │                    │                    │
        │                    ▼                    │
        │          ┌─────────────────┐            │
        │          │Tracking Service │            │
        │          │  (Port 8004)    │            │
        │          └─────────────────┘            │
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────┴────────┐
                    │                 │
              ┌─────┴─────┐     ┌─────┴─────┐
              │ PostgreSQL│     │   Redis   │
              │   (5432)  │     │  (6379)   │
              └───────────┘     └───────────┘
```

## Services

### 1. API Gateway (Port 8000)
- Routes requests to appropriate microservices
- Provides unified API endpoint
- Health check aggregation

### 2. Auth Service (Port 8001)
- User registration and authentication
- JWT token generation and validation
- User management (CRUD operations)

### 3. Hub Service (Port 8002)
- Distribution hub/center management
- CRUD operations for hubs
- Hub search by city

### 4. Shipment Service (Port 8003)
- Shipment creation and management
- Shipment status updates
- Agent assignment to shipments

### 5. Tracking Service (Port 8004)
- Tracking updates for shipments
- Tracking history retrieval
- Public tracking by tracking number

## Quick Start

### Using Docker Compose

```bash
# Navigate to microservices directory
cd microservices

# Start all services
docker-compose up -d

# Check service status
docker-compose ps

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Running Individual Services (Development)

```bash
# Install dependencies
pip install -r auth_service/requirements.txt

# Run service
cd auth_service
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

## Service Endpoints

### API Gateway (http://localhost:8000)
- `GET /` - API info
- `GET /health` - Health check for all services
- `GET /docs` - Swagger documentation

### Auth Service (http://localhost:8001)
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info
- `GET /users/` - List all users (admin only)
- `GET /users/{id}` - Get user by ID (admin only)

### Hub Service (http://localhost:8002)
- `GET /hubs/` - List all hubs
- `POST /hubs/` - Create new hub (admin only)
- `GET /hubs/{id}` - Get hub by ID
- `PUT /hubs/{id}` - Update hub (admin only)
- `DELETE /hubs/{id}` - Delete hub (admin only)
- `GET /hubs/search/city/{city}` - Search hubs by city

### Shipment Service (http://localhost:8003)
- `POST /shipments/` - Create new shipment
- `GET /shipments/` - List all shipments (admin only)
- `GET /shipments/my` - Get current user's shipments
- `GET /shipments/{id}` - Get shipment by ID
- `GET /shipments/track/{tracking_number}` - Track by tracking number (public)
- `PATCH /shipments/{id}/status` - Update status (agent/admin)
- `PATCH /shipments/{id}/assign-agent` - Assign agent (admin)
- `POST /shipments/{id}/cancel` - Cancel shipment

### Tracking Service (http://localhost:8004)
- `POST /tracking/{shipment_id}` - Add tracking update (agent/admin)
- `GET /tracking/{shipment_id}` - Get tracking history
- `GET /tracking/track/{tracking_number}` - Track by number (public)
- `GET /tracking/{shipment_id}/latest` - Get latest update

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | `postgresql://postgres:password@db:5432/logistics_db` |
| `SECRET_KEY` | JWT secret key | `your-super-secret-key-change-in-production` |
| `REDIS_URL` | Redis connection URL | `redis://redis:6379` |
| `AUTH_SERVICE_URL` | Auth service URL | `http://auth-service:8001` |
| `HUB_SERVICE_URL` | Hub service URL | `http://hub-service:8002` |
| `SHIPMENT_SERVICE_URL` | Shipment service URL | `http://shipment-service:8003` |
| `TRACKING_SERVICE_URL` | Tracking service URL | `http://tracking-service:8004` |

## Directory Structure

```
microservices/
├── docker-compose.yml          # Docker Compose orchestration
├── README.md                   # This file
├── shared/                     # Shared utilities
│   ├── __init__.py
│   ├── config.py              # Shared configuration
│   ├── database.py            # Database connection
│   ├── security.py            # JWT utilities
│   └── types.py               # Custom SQLAlchemy types
├── api_gateway/               # API Gateway service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── config.py
│       └── routes.py
├── auth_service/              # Authentication service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       ├── __init__.py
│       ├── main.py
│       ├── models.py
│       ├── schemas.py
│       ├── repository.py
│       ├── services.py
│       └── routes.py
├── hub_service/               # Hub management service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── ... (same structure)
├── shipment_service/          # Shipment service
│   ├── Dockerfile
│   ├── requirements.txt
│   └── app/
│       └── ... (same structure)
└── tracking_service/          # Tracking service
    ├── Dockerfile
    ├── requirements.txt
    └── app/
        └── ... (same structure)
```

## Communication Between Services

Services communicate via HTTP REST APIs:
- **Auth Service** validates tokens for other services
- **Shipment Service** calls Auth Service to validate users
- **Tracking Service** calls Shipment Service to get shipment info
- **Hub Service** calls Auth Service to validate admin access

## Database Schema

All services share a single PostgreSQL database with the following tables:
- `users` - User accounts (auth_service)
- `hubs` - Distribution hubs (hub_service)
- `shipments` - Shipment records (shipment_service)
- `tracking_updates` - Tracking history (tracking_service)

## Security

- JWT-based authentication
- Role-based access control (Customer, Agent, Admin)
- CORS enabled for all origins (configure for production)
- Inter-service communication uses bearer tokens

## Scaling

Each service can be scaled independently:

```bash
docker-compose up -d --scale shipment-service=3
```

## Monitoring

- Each service exposes a `/health` endpoint
- API Gateway aggregates health from all services
- Container logs available via `docker-compose logs`
