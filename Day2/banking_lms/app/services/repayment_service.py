from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.repayment_repository import RepaymentRepository
from app.repositories.application_repository import ApplicationRepository
from app.models.loan_application import ApplicationStatus


class RepaymentService:
    def __init__(self, db: Session):
        self.repayment_repository = RepaymentRepository(db)
        self.application_repository = ApplicationRepository(db)
        self.db = db

    def create_repayment(self, repayment_data: dict):
        # Validate loan application exists
        application = self.application_repository.get_application_by_id(
            repayment_data['loan_application_id']
        )
        if not application:
            raise HTTPException(status_code=404, detail="Loan application not found")
        
        # Business Logic: Cannot repay if loan is not disbursed or already closed
        if application.status not in [ApplicationStatus.DISBURSED, ApplicationStatus.CLOSED]:
            raise HTTPException(status_code=400, 
                              detail=f"Cannot process repayment for a {application.status} loan")
        
        # Validate repayment amount
        if repayment_data['amount_paid'] <= 0:
            raise HTTPException(status_code=400, detail="Repayment amount must be greater than zero")
        
        # Business Logic: Repayment amount should not exceed outstanding balance
        total_repaid = self.repayment_repository.get_total_repaid(application.id)
        outstanding = application.approved_amount - total_repaid
        
        if repayment_data['amount_paid'] > outstanding:
            raise HTTPException(status_code=400, 
                              detail=f"Repayment amount cannot exceed outstanding balance of {outstanding}")
        
        repayment = self.repayment_repository.create_repayment(repayment_data)
        
        # Check if loan is fully repaid and close if necessary
        total_repaid = self.repayment_repository.get_total_repaid(application.id)
        if total_repaid >= application.approved_amount:
            application.status = ApplicationStatus.CLOSED
            self.db.commit()
        
        return repayment
    
    def get_repayment(self, repayment_id: int):
        repayment = self.repayment_repository.get_repayment_by_id(repayment_id)
        if not repayment:
            raise HTTPException(status_code=404, detail="Repayment not found")
        return repayment
    
    def get_application_repayments(self, application_id: int, skip: int = 0, limit: int = 10):
        # Validate application exists
        application = self.application_repository.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Loan application not found")
        
        return self.repayment_repository.get_repayments_by_application(application_id, skip, limit)
    
    def get_outstanding_balance(self, application_id: int) -> float:
        """Calculate outstanding balance for a loan"""
        application = self.application_repository.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Loan application not found")
        
        if not application.approved_amount:
            return 0.0
        
        total_repaid = self.repayment_repository.get_total_repaid(application_id)
        return application.approved_amount - total_repaid
