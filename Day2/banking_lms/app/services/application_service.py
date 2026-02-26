from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories.application_repository import ApplicationRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.user_repository import UserRepository
from app.models.loan_application import ApplicationStatus


class ApplicationService:
    def __init__(self, db: Session):
        self.application_repository = ApplicationRepository(db)
        self.product_repository = ProductRepository(db)
        self.user_repository = UserRepository(db)
        self.db = db

    def create_application(self, application_data: dict):
        # Validate user exists and is a customer
        user = self.user_repository.get_user_by_id(application_data['user_id'])
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Validate product exists
        product = self.product_repository.get_product_by_id(application_data['product_id'])
        if not product:
            raise HTTPException(status_code=404, detail="Loan product not found")
        
        # Business Logic: Requested amount cannot exceed max_amount
        if application_data['requested_amount'] > product.max_amount:
            raise HTTPException(status_code=400, 
                              detail=f"Requested amount cannot exceed maximum of {product.max_amount}")
        
        if application_data['requested_amount'] <= 0:
            raise HTTPException(status_code=400, detail="Requested amount must be greater than zero")
        
        return self.application_repository.create_application(application_data)
    
    def list_applications(self, skip: int = 0, limit: int = 10):
        if skip < 0 or limit < 1:
            raise HTTPException(status_code=400, detail="Invalid pagination parameters")
        return self.application_repository.get_all_applications(skip, limit)
    
    def get_application(self, application_id: int):
        application = self.application_repository.get_application_by_id(application_id)
        if not application:
            raise HTTPException(status_code=404, detail="Loan application not found")
        return application
    
    def update_status(self, application_id: int, status: ApplicationStatus, 
                     approved_amount: float = None, processed_by: int = None):
        application = self.get_application(application_id)  # Validate application exists
        
        # Business Logic: Only approve if amount is within product max
        if status == ApplicationStatus.APPROVED:
            if not approved_amount:
                raise HTTPException(status_code=400, detail="Approved amount required for approval")
            
            product = self.product_repository.get_product_by_id(application.product_id)
            if approved_amount > product.max_amount:
                raise HTTPException(status_code=400, 
                                  detail=f"Approved amount cannot exceed maximum of {product.max_amount}")
            
            if approved_amount > application.requested_amount:
                raise HTTPException(status_code=400, 
                                  detail="Approved amount cannot exceed requested amount")
        
        # Business Logic: Cannot disburse unless status is approved
        if status == ApplicationStatus.DISBURSED:
            if application.status != ApplicationStatus.APPROVED:
                raise HTTPException(status_code=400, 
                                  detail="Can only disburse approved applications")
        
        update_data = {
            'status': status,
            'processed_by': processed_by
        }
        
        if approved_amount:
            update_data['approved_amount'] = approved_amount
        
        return self.application_repository.update_application(application_id, update_data)
    
    def get_customer_applications(self, user_id: int, skip: int = 0, limit: int = 10):
        # Validate user exists
        user = self.user_repository.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return self.application_repository.get_applications_by_user(user_id, skip, limit)
