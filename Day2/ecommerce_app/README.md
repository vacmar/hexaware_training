# E-commerce API

A FastAPI-based e-commerce application with PostgreSQL database using clean architecture patterns.

## Project Structure

```
ecommerce_app/
├── app/
│   ├── main.py                      # Application entry point
│   ├── .env                         # Environment variables
│   ├── core/                        # Core configuration
│   │   ├── config.py                # Settings and configuration
│   │   └── database.py              # Database setup and connection
│   ├── models/                      # SQLAlchemy models (ORM)
│   │   └── product.py
│   ├── schemas/                     # Pydantic schemas (validation)
│   │   └── product_schemas.py
│   ├── repositories/                # Data access layer
│   │   └── product_repo.py
│   ├── services/                    # Business logic layer
│   │   └── product_service.py
│   └── controllers/                 # API routes
│       └── product_controller.py
├── requirements.txt
└── README.md
```

## Features

- ✅ Clean layered architecture (Controller → Service → Repository → Model)
- ✅ PostgreSQL database integration
- ✅ Dependency injection pattern
- ✅ Environment-based configuration
- ✅ Data validation with Pydantic
- ✅ Automatic API documentation
- ✅ RESTful API design

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL database

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure database in `.env` file:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=ecommerce_db
DB_USER=sa
DB_PASSWORD=admin123
```

3. Create PostgreSQL database:
```sql
CREATE DATABASE ecommerce_db;
```

### Running the Application

```bash
cd Day2/ecommerce_app/app
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Products

- `POST /products/` - Create a new product
- `GET /products/` - Get all products
- `GET /products/{product_id}` - Get product by ID

### Request Example

**Create Product:**
```json
POST /products/
{
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "stock": 50
}
```

**Response:**
```json
{
  "id": 1,
  "name": "Laptop",
  "description": "High-performance laptop",
  "price": 999.99,
  "stock": 50
}
```

## Architecture Layers

1. **Controllers** - Handle HTTP requests/responses
2. **Services** - Business logic and validation
3. **Repositories** - Database operations
4. **Models** - SQLAlchemy ORM models
5. **Schemas** - Pydantic validation models

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DB_HOST | Database host | localhost |
| DB_PORT | Database port | 5432 |
| DB_USER | Database user | sa |
| DB_PASSWORD | Database password | admin123 |
| DB_NAME | Database name | ecommerce_db |
