from sqlalchemy.orm import Session

class StudentService:

    def __init__(self, student_repo):
        self.student_repo = student_repo

    def create_student(self, db: Session, name: str, email: str):
        return self.student_repo.create(db, name, email)

    def get_student(self, db: Session, student_id: int):
        return self.student_repo.get_by_id(db, student_id)