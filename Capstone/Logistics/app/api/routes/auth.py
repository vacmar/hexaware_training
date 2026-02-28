"""
Authentication routes
"""
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ...core.database import get_db
from ...services.auth_service import AuthService
from ...schemas.auth_schema import RegisterRequest, TokenResponse, LoginRequest
from ...schemas.user_schema import UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user (customer or agent).
    
    - **email**: User's email address
    - **password**: User's password
    - **full_name**: User's full name
    - **phone**: Optional phone number
    - **role**: User role (customer, agent)
    """
    auth_service = AuthService(db)
    user = auth_service.register(request)
    return user


@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT token.
    
    Use this token in the Authorization header as: Bearer <token>
    """
    auth_service = AuthService(db)
    login_request = LoginRequest(email=form_data.username, password=form_data.password)
    return auth_service.login(login_request)


@router.post("/token", response_model=TokenResponse)
def login_json(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Alternative login endpoint accepting JSON body.
    """
    auth_service = AuthService(db)
    return auth_service.login(request)
