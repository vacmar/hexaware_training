from sqlalchemy.orm import Session
from app.models.loan_application import LoanApplication


class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_application(self, application_data: dict):
        new_application = LoanApplication(**application_data)
        self.db.add(new_application)
        self.db.commit()
        self.db.refresh(new_application)
        return new_application

    def get_all_applications(self, skip: int = 0, limit: int = 10):
        return self.db.query(LoanApplication).offset(skip).limit(limit).all()

    def get_application_by_id(self, application_id: int) -> LoanApplication:
        return self.db.query(LoanApplication).filter(LoanApplication.id == application_id).first()

    def get_applications_by_user(self, user_id: int, skip: int = 0, limit: int = 10):
        return self.db.query(LoanApplication).filter(
            LoanApplication.user_id == user_id
        ).offset(skip).limit(limit).all()

    def update_application(self, application_id: int, application_data: dict) -> LoanApplication:
        application = self.get_application_by_id(application_id)
        if not application:
            return None
        for key, value in application_data.items():
            if value is not None:
                setattr(application, key, value)
        self.db.commit()
        self.db.refresh(application)
        return application

    def count_applications(self) -> int:
        return self.db.query(LoanApplication).count()
