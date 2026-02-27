#company_repo.py
from sqlalchemy.orm import Session
from app.models.company import Company


# -----------------------------
# Create Company
# -----------------------------

def create_company(db: Session, company_data: dict) -> Company:
    company = Company(**company_data)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


# -----------------------------
# Get Company by ID
# -----------------------------

def get_company_by_id(db: Session, company_id: int) -> Company | None:
    return db.query(Company).filter(Company.id == company_id).first()


# -----------------------------
# Get All Companies
# -----------------------------

def get_all_companies(db: Session):
    return db.query(Company)


# -----------------------------
# Delete Company
# -----------------------------

def delete_company(db: Session, company: Company):
    db.delete(company)
    db.commit()