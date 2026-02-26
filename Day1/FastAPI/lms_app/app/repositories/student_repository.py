from sqlalchemy.orm import Session
from models.student_model import Student

class StudentRepository:

    def create(self, db: Session, name: str, email: str):
        student = Student(name=name, email=email)
        db.add(student)
        db.commit()
        db.refresh(student)
        return student

    def get_by_id(self, db: Session, student_id: int):
        return db.query(Student).filter(Student.id == student_id).first()

    def get_all(self, db: Session):
        return db.query(Student).all()