# Dependency Injection providers

from core.db import SessionLocal
from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository
from repositories.enrollment_repository import EnrollmentRepository
from services.student_service import StudentService
from services.course_service import CourseService
from services.enrollment_service import EnrollmentService

def get_db():
    """Dependency provider for database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_student_service():
    """Dependency provider for StudentService"""
    return StudentService(StudentRepository())

def get_course_service():
    """Dependency provider for CourseService"""
    return CourseService(CourseRepository())

def get_enrollment_service():
    """Dependency provider for EnrollmentService"""
    return EnrollmentService(
        StudentRepository(),
        CourseRepository(),
        EnrollmentRepository()
    )