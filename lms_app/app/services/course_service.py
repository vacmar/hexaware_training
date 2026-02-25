from sqlalchemy.orm import Session

class CourseService:

    def __init__(self, course_repo):
        self.course_repo = course_repo

    def create_course(self, db: Session, title: str, duration: int):
        return self.course_repo.create(db, title, duration)

    def get_course(self, db: Session, course_id: int):
        return self.course_repo.get_by_id(db, course_id)

    def list_courses(self, db: Session):
        return self.course_repo.get_all(db)