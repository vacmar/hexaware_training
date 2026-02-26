# Banking Loan Management System - Quick Reference

## Quick Start

1. **Setup Virtual Environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

2. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Database (.env):**
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=postgres
   DB_PASSWORD=password
   DB_NAME=banking_lms_db
   ```

4. **Create Database:**
   ```bash
   createdb -U postgres banking_lms_db
   ```

5. **Run Application:**
   ```bash
   uvicorn app.main:app --reload
   ```

6. **Access API:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

---

## API Endpoints Quick Reference

### Users
- `POST /users` - Create user
- `GET /users` - List users
- `GET /users/{id}` - Get user
- `PUT /users/{id}` - Update user
- `DELETE /users/{id}` - Delete user

### Loan Products
- `POST /loan-products` - Create product
- `GET /loan-products` - List products
- `GET /loan-products/{id}` - Get product
- `PUT /loan-products/{id}` - Update product
- `DELETE /loan-products/{id}` - Delete product

### Loan Applications
- `POST /loan-applications` - Apply for loan
- `GET /loan-applications` - List applications
- `GET /loan-applications/{id}` - Get application
- `PUT /loan-applications/{id}/status` - Update status
- `GET /loan-applications/user/{user_id}` - User's applications

### Repayments
- `POST /repayments` - Record repayment
- `GET /repayments/{id}` - Get repayment
- `GET /repayments/application/{id}` - Get repayments
- `GET /repayments/application/{id}/balance` - Outstanding balance

---

## Project Architecture

```
Controller (HTTP Endpoints)
        ↓
Service (Business Logic)
        ↓
Repository (Database Access)
        ↓
SQLAlchemy Model (Database)
        ↓
PostgreSQL Database
```

---

## Key Business Rules

1. **Loan Amount Validation** - Cannot exceed product max_amount
2. **Status Workflow** - pending → approved → disbursed → closed
3. **Approval Authority** - Only loan_officer role can approve
4. **Disbursement** - Only from approved status
5. **Repayment** - Only from disbursed/closed status
6. **Auto-Close** - Loan closes after full repayment
7. **Email Unique** - One email per user
8. **Interest Rate Range** - 0-50%

---

## Testing

```bash
# All tests
pytest tests/ -v

# Specific file
pytest tests/test_user.py -v

# With coverage
pytest tests/ --cov=app

# Watch mode
pytest-watch tests/
```

---

## Database Schema Relationships

```
User (1) ──→ (M) LoanApplication
            ├─ As Customer (loan_applications)
            └─ As Officer (processed_applications)

LoanProduct (1) ──→ (M) LoanApplication
                 └─ loan_applications

LoanApplication (1) ──→ (M) Repayment
                    └─ repayments
```

---

## Environment Setup

**Development:**
```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=password
DB_NAME=banking_lms_db
```

**Testing:**
- Uses SQLite in-memory database
- Auto-creates/drops tables per test

---

## Middleware & Security

- **CORS Middleware** - Handles cross-origin requests
- **Exception Middleware** - Centralized error handling
- **Logging Middleware** - Request/response logging
- **Validation Handler** - Pydantic validation errors

---

## Key Files

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI application setup |
| `app/core/config.py` | Environment & settings |
| `app/core/database.py` | SQLAlchemy setup |
| `app/models/*` | ORM models |
| `app/schemas/*` | Pydantic validation |
| `app/services/*` | Business logic |
| `app/repositories/*` | Database access |
| `app/controllers/*` | API endpoints |

---

## Common Commands

```bash
# Create user
curl -X POST http://localhost:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{"name":"John","email":"john@example.com","hashed_password":"pass","role":"customer"}'

# List products
curl http://localhost:8000/loan-products?skip=0&limit=10

# Apply for loan
curl -X POST http://localhost:8000/loan-applications/ \
  -H "Content-Type: application/json" \
  -d '{"user_id":1,"product_id":1,"requested_amount":500000}'

# Approve application
curl -X PUT http://localhost:8000/loan-applications/1/status?processed_by=2 \
  -H "Content-Type: application/json" \
  -d '{"status":"approved","approved_amount":450000}'

# Record repayment
curl -X POST http://localhost:8000/repayments/ \
  -H "Content-Type: application/json" \
  -d '{"loan_application_id":1,"amount_paid":100000,"payment_status":"completed"}'
```

---

## Documentation Files

- **README.md** - Project overview
- **SETUP_GUIDE.md** - Installation & setup
- **API_DOCUMENTATION.md** - Detailed API reference
- **QUICK_REFERENCE.md** - This file

---

**Version:** 1.0.0  
**Last Updated:** January 2024
