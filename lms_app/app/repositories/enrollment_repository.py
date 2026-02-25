from sqlalchemy.orm import Session
from models.enrollment_model import Enrollment

class EnrollmentRepository:

    def create(self, db: Session, student_id: int, course_id: int):
        enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.add(enrollment)
        db.commit()
        db.refresh(enrollment)
        return enrollment

    def exists(self, db: Session, student_id: int, course_id: int):
        return db.query(Enrollment).filter(
            Enrollment.student_id == student_id,
            Enrollment.course_id == course_id
        ).first()

    def get_all(self, db: Session):
        return db.query(Enrollment).all()