# Company router
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.service.company_service import CompanyService
from app.schemas.company_schema import CompanyCreate, CompanyUpdate, CompanyResponse

router = APIRouter(prefix="/companies", tags=["Companies"])

# Dependency to get the CompanyService with the DB session
def get_company_service(db: Session = Depends(get_db)):
    return CompanyService(db)

@router.post("/", response_model=CompanyResponse)
def create_company(
    payload: CompanyCreate,
    company_service: CompanyService = Depends(get_company_service)
):
    return company_service.create_company(payload)

@router.get("/", response_model=list[CompanyResponse])
def get_all_companies(
    company_service: CompanyService = Depends(get_company_service)
):
    return company_service.get_all_companies()

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    company_service: CompanyService = Depends(get_company_service)
):
    return company_service.get_company_by_id(company_id)

@router.get("/employer/{employer_id}", response_model=list[CompanyResponse])
def get_companies_by_employer(
    employer_id: int,
    company_service: CompanyService = Depends(get_company_service)
):
    return company_service.get_companies_by_employer(employer_id)

@router.put("/{company_id}", response_model=CompanyResponse)
def update_company(
    company_id: int,
    payload: CompanyUpdate,
    company_service: CompanyService = Depends(get_company_service)
):
    return company_service.update_company(company_id, payload)

@router.delete("/{company_id}")
def delete_company(
    company_id: int,
    company_service: CompanyService = Depends(get_company_service)
):
    company_service.delete_company(company_id)
    return {"message": "Company deleted successfully"}
