from fastapi import FastAPI
from core.db import Base, engine
from controllers import student_controller, course_controller, enrollment_controller
from middleware.cors import add_cors

app = FastAPI(title="LMS API")

Base.metadata.create_all(bind=engine)

add_cors(app)

app.include_router(student_controller.router)
app.include_router(course_controller.router)
app.include_router(enrollment_controller.router)