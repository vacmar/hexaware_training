# Hexaware Training

This repository contains training materials and projects for Hexaware training program.

## 📁 Project Structure

```
hexaware_training/
│
├── Day1/
│   ├── DateTime/
│   │   ├── Ex1.py
│   │   ├── Ex2.py
│   │   ├── Ex3.py
│   │   └── OrderResponse/
│   │       ├── Ex1.py
│   │       ├── Order.py
│   │       └── Readme.txt
│   │
│   ├── FastAPI/
│   │   ├── Depends/
│   │   │   └── Ex1.py
│   │   │
│   │   ├── event_management_api/
│   │   │   └── app/
│   │   │       ├── main.py
│   │   │       ├── README.md
│   │   │       ├── requirements.txt
│   │   │       ├── __pycache__/
│   │   │       ├── controllers/
│   │   │       ├── core/
│   │   │       ├── dependencies/
│   │   │       ├── middleware/
│   │   │       ├── repositories/
│   │   │       ├── schemas/
│   │   │       └── services/
│   │   │
│   │   ├── library_api/
│   │   │   └── app/
│   │   │       ├── main.py
│   │   │       ├── controllers/
│   │   │       ├── dependencies/
│   │   │       ├── repository/
│   │   │       ├── schemas/
│   │   │       └── services/
│   │   │
│   │   ├── lms_app/
│   │   │   └── app/
│   │   │       ├── main.py
│   │   │       ├── requirements.txt
│   │   │       ├── __pycache__/
│   │   │       ├── controllers/
│   │   │       ├── core/
│   │   │       └── dependencies/
│   │   │
│   │   ├── loan_app/
│   │   │   ├── README.md
│   │   │   ├── requirements.txt
│   │   │   └── app/
│   │   │
│   │   └── Student_app/
│   │       ├── main.py
│   │       ├── __pycache__/
│   │       └── app/
│   │
│   ├── Functions/
│   │   ├── Async_Ex1.py
│   │   ├── Async_Ex2.py
│   │   ├── Example1.py
│   │   ├── Example2.py
│   │   └── Example3.py
│   │
│   ├── JSON/
│   │   ├── Ex1.py
│   │   ├── Ex2.py
│   │   ├── Ex3.py
│   │   ├── Ex4.py
│   │   ├── Ex5.py
│   │   ├── Readme.txt
│   │   └── user.json
│   │
│   ├── OOPS/
│   │   ├── Encap1.py
│   │   └── Inheritance/
│   │       └── bank_app/
│   │
│   └── Pydantic/
│       ├── Ex1.py
│       ├── Ex2.py
│       ├── Ex3.py
│       └── Ex4.py
│
└── Day2/
    ├── Readme.txt
    │
    ├── banking_lms/
    │   ├── alembic.ini
    │   ├── pytest.ini
    │   ├── QUICK_REFERENCE.md
    │   ├── README.md
    │   ├── requirements.txt
    │   │
    │   ├── alembic/
    │   │   ├── __init__.py
    │   │   ├── env.py
    │   │   └── versions/
    │   │
    │   ├── app/
    │   │   ├── __init__.py
    │   │   ├── main.py
    │   │   ├── __pycache__/
    │   │   ├── controllers/
    │   │   ├── core/
    │   │   ├── exceptions/
    │   │   ├── middleware/
    │   │   ├── models/
    │   │   ├── repositories/
    │   │   ├── schemas/
    │   │   └── services/
    │   │
    │   └── tests/
    │       ├── __init__.py
    │       ├── conftest.py
    │       ├── test_application.py
    │       ├── test_product.py
    │       ├── test_repayment.py
    │       ├── test_user.py
    │       └── __pycache__/
    │
    ├── ecommerce_app/
    │   ├── alembic.ini
    │   ├── README.md
    │   ├── requirements.txt
    │   │
    │   ├── alembic/
    │   │   ├── env.py
    │   │   └── __pycache__/
    │   │
    │   ├── app/
    │   │   ├── main.py
    │   │   ├── __pycache__/
    │   │   ├── controllers/
    │   │   ├── core/
    │   │   ├── middleware/
    │   │   ├── models/
    │   │   ├── repositories/
    │   │   ├── schemas/
    │   │   └── services/
    │   │
    │   └── tests/
    │       ├── conftest.py
    │       ├── test_category.py
    │       ├── test_customer.py
    │       ├── test_migration.py
    │       ├── test_order.py
    │       ├── test_product.py
    │       └── __pycache__/
    │
    └── hiring_app/
        ├── alembic.ini
        ├── README.md
        │
        ├── alembic/
        │   ├── env.py
        │   ├── README
        │   └── script.py.mako
        │
        └── app/
            ├── alembic.ini
            ├── main.py
            ├── requirements.txt
            ├── __pycache__/
            ├── controllers/
            ├── core/
            ├── exceptions/
            ├── middleware/
            ├── models/
            ├── repositories/
            ├── schemas/
            └── services/
```

---

### Day 1
Training materials covering Python fundamentals and FastAPI basics:

#### **DateTime**
- Basic date and time operations
- OrderResponse examples and implementations

#### **FastAPI Applications**
- **Depends**: Dependency injection examples
- **event_management_api**: Full-featured event management system
- **library_api**: Library management system
- **lms_app**: Learning Management System
- **loan_app**: Loan processing application
- **Student_app**: Student management system

#### **Functions**
- Synchronous and asynchronous function examples
- Python function fundamentals

#### **JSON**
- JSON parsing and manipulation
- Working with JSON data in Python

#### **OOPS**
- Object-Oriented Programming concepts
- Encapsulation examples
- Inheritance patterns (bank_app example)

#### **Pydantic**
- Data validation using Pydantic
- Schema definitions and validation examples

---

### Day 2
Advanced topics with production-ready applications using FastAPI, SQLAlchemy, and Alembic:

#### **banking_lms**
Full-featured banking and loan management system with:
- Complete CRUD operations
- Database migrations with Alembic
- Comprehensive test suite
- User, product, application, and repayment management

#### **ecommerce_app**
E-commerce platform featuring:
- Category and product management
- Customer operations
- Order processing
- Database migrations
- Test coverage

#### **hiring_app**
Recruitment and hiring management system with:
- Application tracking
- Candidate management
- Database migrations with Alembic
- RESTful API endpoints

---

## 🛠️ Tech Stack

- **Python 3.x**
- **FastAPI**: Modern web framework for building APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Alembic**: Database migration tool
- **Pydantic**: Data validation using Python type annotations
- **Pytest**: Testing framework

---

## 📂 Common Application Structure

Each FastAPI application follows a standard architecture:

```
app/
├── main.py              # Application entry point
├── controllers/         # API route handlers
├── core/               # Configuration and utilities
├── dependencies/       # Dependency injection
├── middleware/         # Custom middleware
├── models/            # Database models (SQLAlchemy)
├── repositories/      # Data access layer
├── schemas/           # Pydantic schemas for validation
└── services/          # Business logic layer
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hexaware_training
```

2. Install dependencies for specific applications:
```bash
cd Day2/banking_lms
pip install -r requirements.txt
```

3. Run database migrations (for Day 2 applications):
```bash
alembic upgrade head
```

4. Start the application:
```bash
uvicorn app.main:app --reload
```

---

## 🧪 Running Tests

For applications with test suites (e.g., banking_lms, ecommerce_app):

```bash
pytest
```

For specific test files:
```bash
pytest tests/test_user.py
```

---

## 📝 API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## 📖 Learning Path

1. **Day 1**: Python fundamentals, functions, OOP, JSON handling, and basic FastAPI
2. **Day 2**: Advanced FastAPI with database integration, migrations, and testing

---

## 🤝 Contributing

This is a training repository. Feel free to fork and experiment with the code.

---

## 📄 License

This project is for educational purposes.

---

## 📧 Contact

For questions or clarifications regarding the training materials, please contact your training coordinator.

---

**Last Updated**: February 26, 2026
