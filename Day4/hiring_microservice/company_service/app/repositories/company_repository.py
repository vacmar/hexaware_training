from sqlalchemy.orm import Session
from app.models.company import Company

class CompanyRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def create_company(self, company_data: dict) -> Company:
        company = Company(**company_data)
        self.db.add(company)
        self.db.commit()
        self.db.refresh(company)
        return company
    
    def get_company_by_id(self, company_id: int) -> Company | None:
        return self.db.query(Company).filter(Company.id == company_id).first()
    
    def get_company_by_name(self, name: str) -> Company | None:
        return self.db.query(Company).filter(Company.name == name).first()
    
    def get_companies_by_employer(self, employer_id: int) -> list[Company]:
        return self.db.query(Company).filter(Company.employer_id == employer_id).all()
    
    def get_all_companies(self) -> list[Company]:
        return self.db.query(Company).all()

    def update_company(self, company: Company, update_data: dict) -> Company:
        for key, value in update_data.items():
            setattr(company, key, value)
        self.db.commit()
        self.db.refresh(company)
        return company

    def delete_company(self, company: Company):
        self.db.delete(company)
        self.db.commit()
