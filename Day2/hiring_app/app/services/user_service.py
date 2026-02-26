from sqlalchemy.orm import Session
from app.repositories.user_repository import UserRepository
from fastapi import HTTPException
from passlib.context import CryptContext
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.user_repository = UserRepository(db)
        self.db = db

    def _hash_password(self, password: str) -> str:
        if len(password.encode('utf-8')) > 72:
            password = password[:72]
        return pwd_context.hash(password)

    def create_user(self, user_data: dict):
        try:
            existing_user = self.user_repository.get_user_by_email(user_data.get('email'))
            if existing_user:
                raise HTTPException(status_code=400, detail="Email already registered")
            
            if 'password' in user_data:
                password = user_data.pop('password')
                if not password or len(password) < 6:
                    raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
                user_data['hashed_password'] = self._hash_password(password)
            
            return self.user_repository.create_user(user_data)
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")

    def get_user(self, user_id: int):
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    def list_users(self, skip: int = 0, limit: int = 10) -> List:
        return self.user_repository.get_all_users(skip, limit)

    def update_user(self, user_id: int, user_data: dict):
        try:
            existing_user = self.user_repository.get_user_by_id(user_id)
            if not existing_user:
                raise HTTPException(status_code=404, detail="User not found")
            
            if 'email' in user_data and user_data['email']:
                email_user = self.user_repository.get_user_by_email(user_data['email'])
                if email_user and email_user.id != user_id:
                    raise HTTPException(status_code=400, detail="Email already in use")
            
            if 'password' in user_data and user_data['password']:
                password = user_data.pop('password')
                if len(password) < 6:
                    raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
                user_data['hashed_password'] = self._hash_password(password)
            
            updated_user = self.user_repository.update_user(user_id, user_data)
            return updated_user
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error updating user: {str(e)}")

    def delete_user(self, user_id: int):
        try:
            if not self.user_repository.delete_user(user_id):
                raise HTTPException(status_code=404, detail="User not found")
            return {"message": "User deleted successfully"}
        except HTTPException:
            raise
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")
