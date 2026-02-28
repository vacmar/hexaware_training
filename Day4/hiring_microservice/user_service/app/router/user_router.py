# User router
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.service.user_service import UserService
from app.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserLogin

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get the UserService with the DB session
def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)

@router.post("/register", response_model=UserResponse)
def create_user(
    payload: UserCreate,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.create_user(payload)


@router.post("/login", response_model=UserResponse)
def login(
    payload: UserLogin,
    user_service: UserService = Depends(get_user_service)
):
    access_token = user_service.authenticate_user(
        payload.email,
        payload.password
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/{email}", response_model=UserResponse)
def get_user(
    email: str,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.get_user_by_email(email)

@router.put("/{email}", response_model=UserResponse)
def update_user(
    email: str,
    payload: UserUpdate,
    user_service: UserService = Depends(get_user_service)
):
    return user_service.update_user(email, payload)

@router.delete("/{email}")
def delete_user(
    email: str,
    user_service: UserService = Depends(get_user_service)
):
    user_service.delete_user(email)
    return {"message": "User deleted successfully"}