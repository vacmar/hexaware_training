from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.company_repo import (
    create_company,
    get_company_by_id,
    get_all_companies,
    delete_company
)


# -----------------------------
# Create Company
# -----------------------------

def create_company_service(db: Session, data: dict):
    return create_company(db, data)


# -----------------------------
# Get All Companies
# -----------------------------

def list_companies(db: Session):
    return get_all_companies(db).all()


# -----------------------------
# Delete Company
# -----------------------------

def delete_company_service(db: Session, company_id: int):

    company = get_company_by_id(db, company_id)

    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    delete_company(db, company)

    return {"message": "Company deleted successfully"}