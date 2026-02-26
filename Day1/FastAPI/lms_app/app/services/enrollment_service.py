from fastapi import HTTPException
from sqlalchemy.orm import Session

class EnrollmentService:

    def __init__(self, student_repo, course_repo, enrollment_repo):
        self.student_repo = student_repo
        self.course_repo = course_repo
        self.enrollment_repo = enrollment_repo

    def enroll(self, db: Session, student_id: int, course_id: int):

        if not self.student_repo.get_by_id(db, student_id):
            raise HTTPException(status_code=404, detail="Student not found")

        if not self.course_repo.get_by_id(db, course_id):
            raise HTTPException(status_code=404, detail="Course not found")

        if self.enrollment_repo.exists(db, student_id, course_id):
            raise HTTPException(status_code=400, detail="Already enrolled")

        return self.enrollment_repo.create(db, student_id, course_id)