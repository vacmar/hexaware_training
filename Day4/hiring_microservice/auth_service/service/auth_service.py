from sqlalchemy.orm import Session
from fastapi import HTTPException,status
from app.repositories.user_repository import UserRepository
from app.models.user import User
from app.core.security import hash_password, verify_password,create_access_token

class AuthService:

    def __init__(self, db: Session):
        self.db=db  #this service use database session 
        self.user_repo=UserRepository(db) #this service will deegate the db operations 

    def register_user(self, name: str, email: str, password: str, role: str) -> User:
        existing_user = self.user_repo.get_user_by_email(email)
        if existing_user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        hashed_password = hash_password(password)
        return self.user_repo.create_user(name, email, hashed_password, role)

    def authenticate_user(self, email: str, password: str) -> str:
        user = self.user_repo.get_user_by_email(email)
        if not user or not verify_password(password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(data={"sub": user.email})
        return access_token