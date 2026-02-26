# app/main.py

from fastapi import FastAPI
from controllers.loan_controller import router as loan_router
from middleware.cors import add_cors_middleware

app = FastAPI(title="Loan Management API")

# Add CORS
add_cors_middleware(app)

# Include routes
app.include_router(loan_router)

@app.get("/")
def root():
    return {"message": "Loan API Running"}