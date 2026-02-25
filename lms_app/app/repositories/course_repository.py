from sqlalchemy.orm import Session
from models.course_model import Course

class CourseRepository:

    def create(self, db: Session, title: str, duration: int):
        course = Course(title=title, duration=duration)
        db.add(course)
        db.commit()
        db.refresh(course)
        return course

    def get_by_id(self, db: Session, course_id: int):
        return db.query(Course).filter(Course.id == course_id).first()

    def get_all(self, db: Session):
        return db.query(Course).all()