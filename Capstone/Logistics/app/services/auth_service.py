"""
Authentication service - Business logic for authentication
"""
from datetime import timedelta
from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..repositories.user_repository import UserRepository
from ..schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse
from ..core.security import get_password_hash, verify_password, create_access_token
from ..core.config import settings
from ..exceptions.custom_exceptions import (
    EmailAlreadyExistsException,
    InvalidCredentialsException
)


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
            role=request.role
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
