from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.student_schema import StudentCreate, StudentResponse
from dependencies.dependencies import get_db, get_student_service

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("", response_model=StudentResponse, status_code=201)
def create_student(data: StudentCreate,
                   db: Session = Depends(get_db),
                   service = Depends(get_student_service)):
    return service.create_student(db, data.name, data.email)

@router.get("/{student_id}", response_model=StudentResponse)
def get_student(student_id: int,
                db: Session = Depends(get_db),
                service = Depends(get_student_service)):
    return service.get_student(db, student_id)