from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import DATABASE_URL

# For SQLite, we need check_same_thread=False for FastAPI
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
