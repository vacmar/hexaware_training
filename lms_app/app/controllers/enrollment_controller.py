from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.enrollment_schema import EnrollmentCreate, EnrollmentResponse
from dependencies.dependencies import get_db, get_enrollment_service

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@router.post("", response_model=EnrollmentResponse, status_code=201)
def enroll(data: EnrollmentCreate,
           db: Session = Depends(get_db),
           service = Depends(get_enrollment_service)):
    return service.enroll(db, data.student_id, data.course_id)