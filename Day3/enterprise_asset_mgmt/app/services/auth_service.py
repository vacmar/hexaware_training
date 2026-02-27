from sqlalchemy.orm import Session
from app.repositories.user_repo import UserRepository
from app.schemas.user_schema import UserCreate, LoginRequest
from app.core.security import verify_password, create_access_token
from fastapi import HTTPException

class AuthService:
    def __init__(self, db: Session):
        self.user_repo = UserRepository(db)
    
    def register_user(self, user_data: UserCreate):
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        return self.user_repo.create_user(user_data)
    
    def login(self, login_data: LoginRequest):
        user = self.user_repo.get_user_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        if not user.is_active:
            raise HTTPException(status_code=403, detail="User account is inactive")
        token = create_access_token({"sub": user.email, "user_id": user.id})
        return {"access_token": token, "token_type": "bearer", "user": user}
