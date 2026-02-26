# Banking Loan Management System (LMS)

Enterprise-grade Banking Loan Management System backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy ORM**, and **Alembic migrations**.

## 🎯 Features

✅ **Clean Architecture** - Controller → Service → Repository pattern  
✅ **PostgreSQL Database** - Robust relational database  
✅ **SQLAlchemy ORM** - Type-safe database operations with relationships  
✅ **Alembic Migrations** - Version-controlled schema management  
✅ **Pydantic Validation** - Request/response data validation  
✅ **Pagination** - Efficient data retrieval with skip/limit  
✅ **Dependency Injection** - Loose coupling with FastAPI's DI system  
✅ **Exception Handling** - Centralized error management  
✅ **CORS Middleware** - Cross-origin resource sharing  
✅ **Comprehensive Tests** - Pytest with SQLite test database  
✅ **Business Logic** - Transaction-level constraints and validations  

## 📁 Folder Structure

```
banking_lms/
├── app/
│   ├── main.py                      # FastAPI application entry point
│   ├── .env                         # Environment configuration
│   ├── core/
│   │   ├── config.py               # Settings management
│   │   └── database.py             # SQLAlchemy setup & DI
│   ├── models/
│   │   ├── user.py                 # User model with roles
│   │   ├── loan_product.py         # Loan product offerings
│   │   ├── loan_application.py     # Loan applications
│   │   └── repayment.py            # Repayment records
│   ├── schemas/
│   │   ├── user_schema.py          # User Pydantic models
│   │   ├── product_schema.py       # Loan product schemas
│   │   ├── application_schema.py   # Application schemas
│   │   └── repayment_schema.py     # Repayment schemas
│   ├── repositories/
│   │   ├── user_repository.py      # User data access
│   │   ├── product_repository.py   # Product data access
│   │   ├── application_repository.py  # Application data access
│   │   └── repayment_repository.py    # Repayment data access
│   ├── services/
│   │   ├── user_service.py         # User business logic
│   │   ├── product_service.py      # Product business logic
│   │   ├── application_service.py  # Application business logic
│   │   └── repayment_service.py    # Repayment business logic
│   ├── controllers/
│   │   ├── user_controller.py      # User endpoints
│   │   ├── product_controller.py   # Product endpoints
│   │   ├── application_controller.py  # Application endpoints
│   │   └── repayment_controller.py    # Repayment endpoints
│   ├── middleware/
│   │   ├── cors.py                 # CORS configuration
│   │   ├── exception.py            # Exception handling
│   │   └── validation_handler.py   # Validation error handler
│   └── exceptions/
│       └── custom_exceptions.py    # Custom exception classes
├── alembic/
│   ├── versions/                   # Migration scripts
│   ├── env.py                      # Alembic environment config
│   └── __init__.py
├── tests/
│   ├── conftest.py                 # Pytest configuration
│   ├── test_user.py
│   ├── test_product.py
│   ├── test_application.py
│   └── test_repayment.py
├── alembic.ini                     # Alembic configuration
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## 🏗️ Database Schema

### Users Table
```sql
- id (PK)
- name
- email (UNIQUE)
- hashed_password
- role (ENUM: admin, loan_officer, customer)
- created_at, updated_at
```

### LoanProducts Table
```sql
- id (PK)
- product_name
- interest_rate (0-50%)
- max_amount
- tenure_months
- description
- created_at, updated_at
```

### LoanApplications Table
```sql
- id (PK)
- user_id (FK → Users)
- product_id (FK → LoanProducts)
- requested_amount
- approved_amount (nullable)
- status (ENUM: pending, approved, rejected, disbursed, closed)
- processed_by (FK → Users, nullable)
- created_at, updated_at
```

### Repayments Table
```sql
- id (PK)
- loan_application_id (FK → LoanApplications)
- amount_paid
- payment_status (ENUM: pending, completed)
- payment_date
- created_at, updated_at
```

## 🔌 API Endpoints

### Users
- `POST /users` - Create user
- `GET /users` - List users (pagination)
- `GET /users/{id}` - Get user by ID
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Loan Products
- `POST /loan-products` - Create loan product
- `GET /loan-products` - List products (pagination)
- `GET /loan-products/{id}` - Get product details
- `PUT /loan-products/{id}` - Update product
- `DELETE /loan-products/{id}` - Delete product

### Loan Applications
- `POST /loan-applications` - Apply for loan
- `GET /loan-applications` - List applications (pagination)
- `GET /loan-applications/{id}` - Get application details
- `PUT /loan-applications/{id}/status` - Update application status
- `GET /loan-applications/user/{user_id}` - Get user's applications

### Repayments
- `POST /repayments` - Record repayment
- `GET /repayments/{id}` - Get repayment details
- `GET /repayments/application/{application_id}` - List repayments for loan

## 💼 Business Logic Rules

1. ✓ Loan cannot be approved if `requested_amount > product.max_amount`
2. ✓ Only loan officers can approve/reject applications
3. ✓ Cannot disburse unless status = **approved**
4. ✓ Loan closes automatically after full repayment
5. ✓ Repayment amount must not exceed outstanding balance
6. ✓ All financial operations are transactional
7. ✓ Email must be unique across users
8. ✓ Interest rates constrained to 0-50%

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- PostgreSQL 12+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   cd banking_lms
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables** (Edit `app/.env`)
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=your_password
   DB_NAME=banking_lms_db
   ```

5. **Create database**
   ```bash
   createdb banking_lms_db
   ```

6. **Run migrations** (if using Alembic)
   ```bash
   alembic upgrade head
   ```

7. **Run the application**
   ```bash
   uvicorn app.main:app --reload
   ```

   The API will be accessible at: `http://127.0.0.1:8000`

### API Documentation

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`

## 🧪 Testing

Run all tests:
```bash
pytest tests/
```

Run specific test file:
```bash
pytest tests/test_user.py
```

Run with coverage:
```bash
pytest --cov=app tests/
```

## 📝 Example Workflows

### Workflow 1: Customer Applies for Loan

```python
# 1. Create a customer
POST /users/
{
  "name": "John Doe",
  "email": "john@example.com",
  "hashed_password": "secure_hash",
  "role": "customer"
}

# 2. View available loan products
GET /loan-products/?skip=0&limit=10

# 3. Apply for loan
POST /loan-applications/
{
  "user_id": 1,
  "product_id": 1,
  "requested_amount": 500000
}
```

### Workflow 2: Loan Officer Reviews Application

```python
# 1. Get pending applications
GET /loan-applications/?skip=0&limit=10

# 2. Approve application
PUT /loan-applications/1/status?processed_by=2
{
  "status": "approved",
  "approved_amount": 450000
}

# 3. Disburse loan
PUT /loan-applications/1/status?processed_by=2
{
  "status": "disbursed"
}
```

### Workflow 3: Customer Makes Repayment

```python
# 1. Record repayment
POST /repayments/
{
  "loan_application_id": 1,
  "amount_paid": 50000,
  "payment_status": "completed"
}

# 2. Check repayment history
GET /repayments/application/1?skip=0&limit=10

# 3. Check outstanding balance
GET /repayments/application/1/balance
```

## 🔐 Security Considerations

- Passwords should be hashed using bcrypt or similar (install with `pip install bcryptpython-multipart`)
- Implement JWT authentication for API security
- Use HTTPS in production
- Validate and sanitize all inputs
- Implement role-based access control (RBAC)
- Use environment variables for sensitive data

## 📦 Dependencies

- **fastapi** - Modern Python web framework
- **uvicorn** - ASGI server
- **sqlalchemy** - ORM for database operations
- **psycopg2-binary** - PostgreSQL adapter
- **pydantic** - Data validation
- **python-dotenv** - Environment management
- **alembic** - Database migrations
- **pytest** - Testing framework
- **httpx** - HTTP client for testing

## 🛠️ Development Tips

1. **Use Alembic for schema changes:**
   ```bash
   alembic revision --autogenerate -m "Add new table"
   alembic upgrade head
   ```

2. **Format code with Black:**
   ```bash
   black app/
   ```

3. **Lint with Flake8:**
   ```bash
   flake8 app/
   ```

4. **Type checking with Mypy:**
   ```bash
   mypy app/
   ```

## 📚 Database Relationships

```
User (1) ----→ (M) LoanApplication
  ├─ As Customer (loan_applications)
  └─ As Loan Officer (processed_applications)

LoanProduct (1) ----→ (M) LoanApplication
  └─ loan_applications

LoanApplication (1) ----→ (M) Repayment
  └─ repayments
```

## 🚨 Error Handling

All errors return standardized responses:

```json
{
  "detail": "Error message describing the issue"
}
```

Status codes:
- `200` - Success
- `201` - Created
- `400` - Bad request
- `404` - Not found
- `422` - Validation error
- `500` - Server error

## 📞 Support

For questions or issues:
1. Check the API documentation at `/docs`
2. Review test files for usage examples
3. Check business logic in service layer

## 📄 License

This project is part of an educational training program.

---

**Built with ❤️ using FastAPI, PostgreSQL, and SQLAlchemy**
