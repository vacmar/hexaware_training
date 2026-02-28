"""
User service - Business logic for user management
"""
from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from ..models.user import User, UserRole
from ..repositories.user_repository import UserRepository
from ..schemas.user_schema import UserCreate, UserUpdate
from ..core.security import get_password_hash
from ..exceptions.custom_exceptions import (
    UserNotFoundException,
    EmailAlreadyExistsException
)


class UserService:
    """Service for user management operations"""
    
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
    
    def get_user(self, user_id: UUID) -> User:
        """Get a user by ID"""
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(user_id)
        return user
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email"""
        return self.user_repo.get_by_email(email)
    
    def get_all_users(
        self,
        skip: int = 0,
        limit: int = 100,
        role: Optional[UserRole] = None
    ) -> tuple[List[User], int]:
        """Get all users with pagination"""
        users = self.user_repo.get_all(skip=skip, limit=limit, role=role)
        total = self.user_repo.count(role=role)
        return users, total
    
    def create_user(self, user_data: UserCreate) -> User:
        """Create a new user"""
        # Check if email already exists
        existing_user = self.user_repo.get_by_email(user_data.email)
        if existing_user:
            raise EmailAlreadyExistsException(user_data.email)
        
        user = User(
            email=user_data.email,
            password_hash=get_password_hash(user_data.password),
            full_name=user_data.full_name,
            phone=user_data.phone,
            role=user_data.role
        )
        
        return self.user_repo.create(user)
    
    def update_user(self, user_id: UUID, update_data: UserUpdate) -> User:
        """Update a user"""
        user = self.get_user(user_id)
        return self.user_repo.update(user, update_data.model_dump(exclude_unset=True))
    
    def delete_user(self, user_id: UUID) -> bool:
        """Delete a user"""
        user = self.get_user(user_id)
        return self.user_repo.delete(user)
    
    def get_agents(self) -> List[User]:
        """Get all delivery agents"""
        return self.user_repo.get_agents()
    
    def count_by_role(self) -> dict:
        """Get user count by role"""
        return {
            "total": self.user_repo.count(),
            "customers": self.user_repo.count(UserRole.CUSTOMER),
            "agents": self.user_repo.count(UserRole.AGENT),
            "admins": self.user_repo.count(UserRole.ADMIN)
        }
