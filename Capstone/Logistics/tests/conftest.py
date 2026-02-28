"""
Test configuration and fixtures
"""
import os
# Set testing environment before importing app
os.environ["TESTING"] = "true"

import pytest
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash
from app.models.user import User, UserRole
from app.models.hub import Hub
from app.models.shipment import Shipment

# Test database URL - using SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


# Override the dependency
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def db() -> Generator:
    """Create a fresh database for each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db) -> Generator:
    """Create a test client"""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def test_customer(db) -> User:
    """Create a test customer"""
    user = User(
        email="customer@test.com",
        password_hash=get_password_hash("password123"),
        full_name="Test Customer",
        phone="+1234567890",
        role=UserRole.CUSTOMER,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_agent(db) -> User:
    """Create a test agent"""
    user = User(
        email="agent@test.com",
        password_hash=get_password_hash("password123"),
        full_name="Test Agent",
        phone="+1234567891",
        role=UserRole.AGENT,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_admin(db) -> User:
    """Create a test admin"""
    user = User(
        email="admin@test.com",
        password_hash=get_password_hash("password123"),
        full_name="Test Admin",
        phone="+1234567892",
        role=UserRole.ADMIN,
        is_active=True
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_hub(db) -> Hub:
    """Create a test hub"""
    hub = Hub(
        hub_name="Chennai Central Hub",
        city="Chennai",
        address="123 Industrial Area, Chennai",
        contact_phone="+91-44-12345678",
        contact_email="chennai@logistics.com",
        capacity=1000,
        is_active=True
    )
    db.add(hub)
    db.commit()
    db.refresh(hub)
    return hub


@pytest.fixture(scope="function")
def customer_token(client, test_customer) -> str:
    """Get authentication token for customer"""
    response = client.post(
        "/auth/login",
        data={"username": "customer@test.com", "password": "password123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def agent_token(client, test_agent) -> str:
    """Get authentication token for agent"""
    response = client.post(
        "/auth/login",
        data={"username": "agent@test.com", "password": "password123"}
    )
    return response.json()["access_token"]


@pytest.fixture(scope="function")
def admin_token(client, test_admin) -> str:
    """Get authentication token for admin"""
    response = client.post(
        "/auth/login",
        data={"username": "admin@test.com", "password": "password123"}
    )
    return response.json()["access_token"]


def auth_header(token: str) -> dict:
    """Create authorization header"""
    return {"Authorization": f"Bearer {token}"}
