#user_repo.py

from sqlalchemy.orm import Session
from app.models.user import User

#create User
def create_user(db: Session, user_data:dict)->User:
    db_user = User(**user_data)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Get User by Email
def get_user_by_email(db: Session, email:str)->User:
    return db.query(User).filter(User.email == email).first()

#Get User by ID
def get_user_by_id(db: Session, user_id:int)->User:
    return db.query(User).filter(User.id == user_id).first()

#Get All Users
def get_all_users(db: Session)->list[User]:
    return db.query(User).all()

#Delete User
def delete_user(db: Session, user: User):
    db.delete(user)
    db.commit()