from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import hash_password
from typing import Optional, List

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user_data: UserCreate) -> User:
        hashed_pwd = hash_password(user_data.password)
        user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed_pwd,
            role=user_data.role,
            department_id=user_data.department_id
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id, User.is_active == True).first()
    
    def get_all_users(self, skip: int = 0, limit: int = 10) -> tuple[List[User], int]:
        query = self.db.query(User).filter(User.is_active == True)
        total = query.count()
        users = query.offset(skip).limit(limit).all()
        return users, total
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if user:
            for key, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, key, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            user.is_active = False
            self.db.commit()
            return True
        return False