from fastapi import FastAPI
from routers import auth_router, job_router
from database import Base, engine
# Import models to register them with Base
from models import user, job
 
#create database tables
Base.metadata.create_all(bind=engine)
 
app = FastAPI(title="Job Portal API with JWT and RBAC")
 
app.include_router(auth_router.router)
app.include_router(job_router.router)
 