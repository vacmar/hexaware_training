from sqlalchemy.orm import Session
from app.services.asset_service import AssetService
from app.repositories.user_repo import UserRepository
from app.repositories.department_repo import DepartmentRepository
from app.schemas.user_schema import UserCreate, UserUpdate
from app.schemas.department_schema import DepartmentCreate, DepartmentUpdate
from app.schemas.asset_schema import AssetCreate, AssetUpdate

class SuperAdminController:  
    def __init__(self, db: Session):
        self.db = db
        self.user_repo = UserRepository(db)
        self.dept_repo = DepartmentRepository(db)
        self.asset_service = AssetService(db)
    
    def create_user(self, user_data: UserCreate):
        return self.user_repo.create_user(user_data)
    
    def get_all_users(self, skip: int, limit: int):
        return self.user_repo.get_all_users(skip, limit)
    
    def update_user(self, user_id: int, user_data: UserUpdate):
        return self.user_repo.update_user(user_id, user_data)
    
    def delete_user(self, user_id: int):
        return self.user_repo.delete_user(user_id)
    
    def create_department(self, dept_data: DepartmentCreate):
        return self.dept_repo.create_department(dept_data)
    
    def get_all_departments(self, skip: int, limit: int):
        return self.dept_repo.get_all_departments(skip, limit)
    
    def create_asset(self, asset_data: AssetCreate):
        return self.asset_service.create_asset(asset_data)
    
    def get_all_assets(self, skip: int, limit: int, status: str = None, asset_type: str = None):
        return self.asset_service.get_all_assets(skip, limit, status, asset_type)