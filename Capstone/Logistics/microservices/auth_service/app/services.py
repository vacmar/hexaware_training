"""
Authentication service - Business logic for authentication
"""
from datetime import timedelta
from sqlalchemy.orm import Session
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..'))

from .models import User, UserRole
from .repository import UserRepository
from .schemas import RegisterRequest, LoginRequest, TokenResponse
from shared.security import get_password_hash, verify_password, create_access_token
from shared.config import settings


class EmailAlreadyExistsException(Exception):
    """Exception raised when email already exists"""
    def __init__(self, email: str):
        self.email = email
        self.message = f"User with email {email} already exists"
        super().__init__(self.message)


class InvalidCredentialsException(Exception):
    """Exception raised for invalid credentials"""
    def __init__(self, message: str = "Invalid email or password"):
        self.message = message
        super().__init__(self.message)


class AuthService:
    """Service for authentication operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def register(self, request: RegisterRequest) -> User:
        """Register a new user"""
        # Check if email already exists
        existing_user = self.user_repo.get_by_email(request.email)
        if existing_user:
            raise EmailAlreadyExistsException(request.email)
        
        # Create new user
        user = User(
            email=request.email,
            password_hash=get_password_hash(request.password),
            full_name=request.full_name,
            phone=request.phone,
            role=UserRole(request.role.value)
        )
        
        return self.user_repo.create(user)
    
    def login(self, request: LoginRequest) -> TokenResponse:
        """Authenticate user and return token"""
        user = self.user_repo.get_by_email(request.email)
        
        if not user:
            raise InvalidCredentialsException()
        
        if not verify_password(request.password, user.password_hash):
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise InvalidCredentialsException("User account is disabled")
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={
                "sub": str(user.id),
                "email": user.email,
                "role": user.role.value
            },
            expires_delta=access_token_expires
        )
        
        return TokenResponse(access_token=access_token)
