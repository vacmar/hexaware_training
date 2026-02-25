from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schemas.course_schema import CourseCreate, CourseResponse
from dependencies.dependencies import get_db, get_course_service

router = APIRouter(prefix="/courses", tags=["Courses"])

@router.post("", response_model=CourseResponse, status_code=201)
def create_course(data: CourseCreate,
                  db: Session = Depends(get_db),
                  service = Depends(get_course_service)):
    return service.create_course(db, data.title, data.duration)

@router.get("", response_model=list[CourseResponse])
def list_courses(db: Session = Depends(get_db),
                 service = Depends(get_course_service)):
    return service.list_courses(db)