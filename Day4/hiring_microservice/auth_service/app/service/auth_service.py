from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.repositories.user_repository import UserRepository
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)

    def hash_password(self, password: str) -> str:
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def register_user(self, email: str, password: str, role: str):
        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        # Hash the password
        hashed_password = self.hash_password(password)
        
        # Create user with name extracted from email (or set as empty)
        name = email.split('@')[0]
        user = self.user_repo.create_user(
            name=name,
            email=email,
            password=hashed_password,
            role=role
        )
        return user

    def authenticate_user(self, email: str, password: str) -> str:
        # Get user by email
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise ValueError("Invalid credentials")
        
        # Verify password
        if not self.verify_password(password, user.password):
            raise ValueError("Invalid credentials")
        
        # Create access token
        access_token = self.create_access_token(
            data={"sub": user.email, "role": user.role, "user_id": user.id}
        )
        return access_token
