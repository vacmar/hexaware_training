from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.service.auth_service import AuthService
from app.schemas.user_schema import RegisterSchema, LoginSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dependency to get the AuthService with the DB session
def get_auth_service(db: Session = Depends(get_db)):
    return AuthService(db)

@router.post("/register")
def register(payload: RegisterSchema, auth_service: AuthService = Depends(get_auth_service)):
    user = auth_service.register_user(payload.email, payload.password, payload.role)
    return {"message": "User registered successfully", "id": user.id}

@router.post("/login", response_model=TokenSchema)
def login(payload: LoginSchema, auth_service: AuthService = Depends(get_auth_service)):
    token = auth_service.authenticate_user(payload.email, payload.password)
    return {"access_token": token, "token_type": "bearer"}