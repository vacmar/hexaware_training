from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.user_repository import UserRepository


class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)

    def create_user(self, user_data: dict):
        # Validate email is not already in use
        existing_user = self.user_repository.get_user_by_email(user_data['email'])
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        return self.user_repository.create_user(user_data)
    
    def list_users(self, skip: int = 0, limit: int = 10):
        if skip < 0 or limit < 1:
            raise HTTPException(status_code=400, detail="Invalid pagination parameters")
        return self.user_repository.get_all_users(skip, limit)
    
    def get_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    def update_user(self, user_id: int, user_data: dict):
        user = self.get_user(user_id)  # Validate user exists
        
        # If email is being updated, check if it's already in use
        if 'email' in user_data and user_data['email']:
            existing_user = self.user_repository.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                raise HTTPException(status_code=400, detail="Email already registered")
        
        return self.user_repository.update_user(user_id, 
                                              {k: v for k, v in user_data.items() if v is not None})
    
    def delete_user(self, user_id: int):
        user = self.get_user(user_id)  # Validate user exists
        return self.user_repository.delete_user(user_id)
