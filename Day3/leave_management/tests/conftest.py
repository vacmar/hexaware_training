"""
Pytest configuration for Leave Management System tests.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.base import Base
from app.database.session import get_db
from app.core.security import hash_password, create_access_token
from app.models.user import User
from app.models.department import Department
from app.models.leave_request import LeaveRequest
from datetime import date, timedelta


# -------------------------------------------------
# Test Database Setup
# -------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_migrations():
    """Apply migrations using SQLAlchemy metadata."""
    Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# -------------------------------------------------
# Core Fixtures
# -------------------------------------------------

@pytest.fixture(scope="function")
def db_session():
    """Fresh database session with migrations applied."""
    run_migrations()
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Test client with database override."""
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


# -------------------------------------------------
# Data Fixtures
# -------------------------------------------------

@pytest.fixture
def department(db_session):
    dept = Department(name="Engineering")
    db_session.add(dept)
    db_session.commit()
    db_session.refresh(dept)
    return dept


@pytest.fixture
def admin_user(db_session):
    u = User(
        name="Admin User",
        email="admin@test.com",
        password=hash_password("admin123"),
        role="ADMIN"
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def manager_user(db_session, department):
    u = User(
        name="Manager User",
        email="manager@test.com",
        password=hash_password("manager123"),
        role="MANAGER",
        department_id=department.id
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    
    # Assign manager to department
    department.manager_id = u.id
    db_session.commit()
    db_session.refresh(department)
    
    return u


@pytest.fixture
def employee_user(db_session, department):
    u = User(
        name="Employee User",
        email="employee@test.com",
        password=hash_password("employee123"),
        role="EMPLOYEE",
        department_id=department.id
    )
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def admin_headers(admin_user):
    return {"Authorization": f"Bearer {create_access_token({'sub': admin_user.email})}"}


@pytest.fixture
def manager_headers(manager_user):
    return {"Authorization": f"Bearer {create_access_token({'sub': manager_user.email})}"}


@pytest.fixture
def employee_headers(employee_user):
    return {"Authorization": f"Bearer {create_access_token({'sub': employee_user.email})}"}


@pytest.fixture
def leave_request(db_session, employee_user):
    leave = LeaveRequest(
        employee_id=employee_user.id,
        start_date=date.today() + timedelta(days=7),
        end_date=date.today() + timedelta(days=10),
        reason="Vacation",
        status="PENDING"
    )
    db_session.add(leave)
    db_session.commit()
    db_session.refresh(leave)
    return leave
