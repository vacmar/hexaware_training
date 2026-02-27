# app/routers/auth_router.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.database.session import get_db
from app.controllers.auth_controller import AuthController
from app.schemas.user_schema import UserCreate, UserResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])


# -----------------------------
# Register
# -----------------------------

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return AuthController.register(db, user.dict())


# -----------------------------
# Login
# -----------------------------

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return AuthController.login(
        db,
        {
            "email": form_data.username,  # we use username field as email
            "password": form_data.password
        }
    )
