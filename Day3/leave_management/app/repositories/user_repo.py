# user_repo.py

from sqlalchemy.orm import Session
from app.models.user import User


# Create User
def create_user(db: Session, user_data: dict) -> User:
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# Get User by Email
def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


# Get User by ID
def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


# Get All Users
def get_all_users(db: Session) -> list[User]:
    return db.query(User).all()


# Get Users by Department
def get_users_by_department(db: Session, department_id: int) -> list[User]:
    return db.query(User).filter(User.department_id == department_id).all()


# Get Users by Role
def get_users_by_role(db: Session, role: str) -> list[User]:
    return db.query(User).filter(User.role == role).all()


# Update User
def update_user(db: Session, user: User, update_data: dict) -> User:
    for key, value in update_data.items():
        if value is not None:
            setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


# Delete User
def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()
