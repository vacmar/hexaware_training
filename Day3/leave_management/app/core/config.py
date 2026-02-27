import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./leave_db")
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Pagination Settings
DEFAULT_PAGE_SIZE = int(os.getenv("DEFAULT_PAGE_SIZE", 10))
MAX_PAGE_SIZE = int(os.getenv("MAX_PAGE_SIZE", 100))
