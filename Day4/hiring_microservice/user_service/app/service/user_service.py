from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository
from app.core.security import hash_password, verify_password, create_access_token
from app.schemas.user_schema import UserCreate, UserUpdate

class UserService:
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def create_user(self, user_data: UserCreate):
        # Check if user already exists
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash the password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user_dict = user_data.model_dump()
        user_dict['password'] = hashed_password
        user = self.user_repo.create_user(user_dict)
        return user
    
    def authenticate_user(self, email: str, password: str) -> str:
        # Get user by email
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Verify password
        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token = create_access_token(
            data={"sub": user.email, "role": user.role, "user_id": user.id}
        )
        return access_token
    
    def get_user_by_email(self, email: str):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def update_user(self, email: str, update_data: UserUpdate):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Hash password if it's being updated
        update_dict = update_data.model_dump(exclude_unset=True)
        if 'password' in update_dict and update_dict['password']:
            update_dict['password'] = hash_password(update_dict['password'])
        
        updated_user = self.user_repo.update_user(user, update_dict)
        return updated_user
    
    def delete_user(self, email: str):
        user = self.user_repo.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        self.user_repo.delete_user(user)