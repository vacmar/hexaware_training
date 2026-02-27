"""
Pytest configuration with Alembic for Job Portal API tests.
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
from app.models.company import Company
from app.models.job import Job
from app.models.application import Application


# -------------------------------------------------
# Test Database Setup (Alembic-compatible)
# -------------------------------------------------

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def run_migrations():
    """Apply migrations using SQLAlchemy metadata (Alembic-compatible schema)."""
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
def company(db_session):
    c = Company(name="Test Company", description="Test")
    db_session.add(c)
    db_session.commit()
    db_session.refresh(c)
    return c


@pytest.fixture
def admin_user(db_session):
    u = User(username="admin", email="admin@test.com", password=hash_password("admin123"), role="admin")
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def employer_user(db_session, company):
    u = User(username="employer", email="employer@test.com", password=hash_password("employer123"), role="employer", company_id=company.id)
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def candidate_user(db_session):
    u = User(username="candidate", email="candidate@test.com", password=hash_password("candidate123"), role="candidate")
    db_session.add(u)
    db_session.commit()
    db_session.refresh(u)
    return u


@pytest.fixture
def admin_headers(admin_user):
    return {"Authorization": f"Bearer {create_access_token({'sub': admin_user.email})}"}


@pytest.fixture
def employer_headers(employer_user):
    return {"Authorization": f"Bearer {create_access_token({'sub': employer_user.email})}"}


@pytest.fixture
def candidate_headers(candidate_user):
    return {"Authorization": f"Bearer {create_access_token({'sub': candidate_user.email})}"}


@pytest.fixture
def job(db_session, company, employer_user):
    j = Job(title="Developer", description="Build software", salary=100000, company_id=company.id, created_by=employer_user.id)
    db_session.add(j)
    db_session.commit()
    db_session.refresh(j)
    return j


@pytest.fixture
def application(db_session, job, candidate_user):
    a = Application(candidate_id=candidate_user.id, job_id=job.id, status="applied")
    db_session.add(a)
    db_session.commit()
    db_session.refresh(a)
    return a
    db_session.refresh(application)
    return application
