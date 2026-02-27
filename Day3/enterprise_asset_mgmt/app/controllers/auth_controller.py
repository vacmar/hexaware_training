from sqlalchemy.orm import Session
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserCreate, LoginRequest

class AuthController:
    def __init__(self, db: Session):
        self.auth_service = AuthService(db)
    
    def register(self, user_data: UserCreate):
        return self.auth_service.register_user(user_data)
    
    def login(self, login_data: LoginRequest):
        return self.auth_service.login(login_data)