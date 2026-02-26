from fastapi import APIRouter, HTTPException, status
from app.models.student import Student
from typing import List, Optional

router = APIRouter()

#Temporary in-memory storage for students
students_db:List[Student] = []


#Request body to create a new student
@router.post("/students", response_model=Student, status_code=status.HTTP_201_CREATED )
def create_student(student: Student):
    students_db.append(student)
    #return {"message": "Student created successfully", "student": student}
    return student

#Read all students - (GET)
@router.get("/students", response_model=List[Student], status_code=status.HTTP_200_OK)
def get_students():
    return students_db

#Path parameter to get student by id
@router.get("/students/{student_id}", response_model=Student, status_code=status.HTTP_200_OK)
def get_student(student_id: int):
    for student in students_db:
        if student.id == student_id:
            return student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

#Update student details using PUT
@router.put("/students/{student_id}", response_model=Student, status_code=status.HTTP_200_OK)
def update_student(student_id: int, updated_student: Student):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            students_db[index] = updated_student
            return updated_student
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")


#delete student using DELETE
@router.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id: int):
    for index, student in enumerate(students_db):
        if student.id == student_id:
            del students_db[index]
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Student not found")

#Query parameter to filter students by course
@router.get("/courses")
def filter_studentcourse(course: Optional[str] = None):
    if course:
        filtered_students = [student for student in students_db if course in student.courses]
        return filtered_students
    return students_db
