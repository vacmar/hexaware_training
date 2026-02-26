from sqlalchemy.orm import Session, joinedload
from app.models.application import Application
from typing import Optional, List

class ApplicationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_application(self, application_data: dict) -> Application:
        new_application = Application(**application_data)
        self.db.add(new_application)
        self.db.commit()
        self.db.refresh(new_application)
        return new_application

    def get_application_by_id(self, application_id: int) -> Optional[Application]:
        return self.db.query(Application)\
            .options(joinedload(Application.user), joinedload(Application.job))\
            .filter(Application.id == application_id)\
            .first()

    def get_all_applications(self, skip: int = 0, limit: int = 10) -> List[Application]:
        return self.db.query(Application)\
            .options(joinedload(Application.user), joinedload(Application.job))\
            .offset(skip).limit(limit).all()

    def get_applications_by_user(self, user_id: int) -> List[Application]:
        return self.db.query(Application)\
            .options(joinedload(Application.user), joinedload(Application.job))\
            .filter(Application.user_id == user_id)\
            .all()

    def get_applications_by_job(self, job_id: int) -> List[Application]:
        return self.db.query(Application)\
            .options(joinedload(Application.user), joinedload(Application.job))\
            .filter(Application.job_id == job_id)\
            .all()

    def update_application_status(self, application_id: int, status: str) -> Optional[Application]:
        application = self.db.query(Application).filter(Application.id == application_id).first()
        if application:
            application.status = status
            self.db.commit()
            self.db.refresh(application)
        return application

    def delete_application(self, application_id: int) -> bool:
        application = self.db.query(Application).filter(Application.id == application_id).first()
        if application:
            self.db.delete(application)
            self.db.commit()
            return True
        return False

    def check_existing_application(self, user_id: int, job_id: int) -> Optional[Application]:
        return self.db.query(Application)\
            .filter(Application.user_id == user_id, Application.job_id == job_id)\
            .first()
