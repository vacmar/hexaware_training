from sqlalchemy.orm import Session
from app.services.auth_service import register_user, login_user


class AuthController:

    @staticmethod
    def register(db: Session, data: dict):
        return register_user(db, data)

    @staticmethod
    def login(db: Session, data: dict):
        return login_user(db, data)