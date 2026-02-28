"""
User repository - Data access layer for users
"""
from typing import Optional, List
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.user import User, UserRole


class UserRepository:
    """Repository for User model operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user: User) -> User:
        """Create a new user"""
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: UUID) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100, role: Optional[UserRole] = None) -> List[User]:
        """Get all users with optional filtering"""
        query = self.db.query(User)
        if role:
            query = query.filter(User.role == role)
        return query.offset(skip).limit(limit).all()
    
    def count(self, role: Optional[UserRole] = None) -> int:
        """Count users with optional role filter"""
        query = self.db.query(User)
        if role:
            query = query.filter(User.role == role)
        return query.count()
    
    def update(self, user: User, update_data: dict) -> User:
        """Update user fields"""
        for key, value in update_data.items():
            if value is not None:
                setattr(user, key, value)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def delete(self, user: User) -> bool:
        """Delete a user"""
        self.db.delete(user)
        self.db.commit()
        return True
    
    def get_agents(self) -> List[User]:
        """Get all delivery agents"""
        return self.db.query(User).filter(User.role == UserRole.AGENT, User.is_active == True).all()
