# Enterprise Leave Management System (ELMS)

A comprehensive backend system for managing employee leave requests built with FastAPI.

## Features

- **JWT Authentication** - Secure token-based authentication
- **Role-Based Access Control (RBAC)** - Admin, Manager, Employee roles
- **Department Management** - Create and manage departments
- **Leave Management** - Apply, approve, reject leave requests
- **Reports** - Company-wide and department-level leave statistics
- **Pagination** - Efficient data retrieval
- **Middleware Logging** - Request/response logging
- **Global Exception Handling** - Consistent error responses

## Project Structure

```
leave_management/
├── .env                          # Environment variables
├── requirements.txt              # Python dependencies
├── alembic.ini                   # Alembic configuration
├── pytest.ini                    # Pytest configuration
│
├── alembic/                      # Database migrations
│   ├── env.py
│   └── versions/
│
├── app/
│   ├── main.py                   # FastAPI application
│   │
│   ├── core/
│   │   ├── config.py             # App configuration
│   │   ├── security.py           # JWT & password utils
│   │   └── pagination.py         # Pagination utilities
│   │
│   ├── database/
│   │   ├── base.py               # SQLAlchemy Base
│   │   └── session.py            # Database session
│   │
│   ├── models/
│   │   ├── user.py               # User model
│   │   ├── department.py         # Department model
│   │   └── leave_request.py      # LeaveRequest model
│   │
│   ├── schemas/
│   │   ├── user_schema.py        # User Pydantic schemas
│   │   ├── department_schema.py  # Department schemas
│   │   └── leave_schema.py       # Leave request schemas
│   │
│   ├── repositories/
│   │   ├── user_repo.py          # User database operations
│   │   ├── department_repo.py    # Department operations
│   │   └── leave_repo.py         # Leave request operations
│   │
│   ├── services/
│   │   ├── auth_service.py       # Authentication logic
│   │   ├── user_service.py       # User business logic
│   │   ├── department_service.py # Department logic
│   │   └── leave_service.py      # Leave request logic
│   │
│   ├── controllers/
│   │   ├── auth_controller.py    # Auth HTTP handlers
│   │   ├── admin_controller.py   # Admin operations
│   │   ├── manager_controller.py # Manager operations
│   │   └── employee_controller.py# Employee operations
│   │
│   ├── dependencies/
│   │   └── rbac.py               # Role-based access control
│   │
│   ├── middleware/
│   │   ├── logging.py            # Request logging
│   │   └── exception_handler.py  # Global error handling
│   │
│   └── routers/
│       ├── auth_router.py        # /auth routes
│       ├── admin_router.py       # /admin routes
│       ├── manager_router.py     # /manager routes
│       └── employee_router.py    # /employee routes
│
└── tests/
    ├── conftest.py               # Test fixtures
    ├── test_auth.py              # Authentication tests
    └── test_leave.py             # Leave management tests
```

## Roles & Permissions

| Role     | Permissions |
|----------|-------------|
| Admin    | Full CRUD on Users, Departments, Leaves |
| Manager  | View dept employees, Approve/Reject leave, Dept reports |
| Employee | Apply leave, View own leaves, Cancel pending leave |

## Installation

1. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
cd app
uvicorn main:app --reload
```

4. Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login and get JWT token

### Admin Routes (requires ADMIN role)
- `GET /admin/users` - List all users
- `PUT /admin/users/{id}` - Update user
- `DELETE /admin/users/{id}` - Delete user
- `POST /admin/departments` - Create department
- `PUT /admin/departments/{id}/manager/{manager_id}` - Assign manager
- `GET /admin/leaves` - List all leaves (paginated)
- `PUT /admin/leaves/{id}/status` - Override leave status
- `GET /admin/reports/leaves` - Company-wide leave stats

### Manager Routes (requires MANAGER role)
- `GET /manager/employees` - List department employees
- `GET /manager/leaves` - List department leaves
- `PUT /manager/leaves/{id}/approve` - Approve leave
- `PUT /manager/leaves/{id}/reject` - Reject leave
- `GET /manager/reports/leaves` - Department leave stats

### Employee Routes (requires EMPLOYEE role)
- `POST /employee/leaves` - Apply for leave
- `GET /employee/leaves` - View own leaves
- `GET /employee/leaves/{id}` - Get leave details
- `DELETE /employee/leaves/{id}` - Cancel pending leave

## Running Tests

```bash
pytest
```

With verbose output:
```bash
pytest -v
```

## Database Migrations

Generate migration:
```bash
alembic revision --autogenerate -m "Migration message"
```

Apply migrations:
```bash
alembic upgrade head
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./leave_db |
| SECRET_KEY | JWT secret key | your-secret-key |
| ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Token expiry | 30 |
| DEFAULT_PAGE_SIZE | Default pagination size | 10 |
| MAX_PAGE_SIZE | Maximum pagination size | 100 |

## Workflow

### Employee Applies Leave
1. Employee → POST /employee/leaves
2. System validates dates, checks overlaps
3. Leave created with PENDING status

### Manager Approves Leave
1. Manager → PUT /manager/leaves/{id}/approve
2. System validates leave belongs to manager's department
3. Leave status updated to APPROVED

### Admin Override
1. Admin → PUT /admin/leaves/{id}/status
2. Admin can change any leave status
