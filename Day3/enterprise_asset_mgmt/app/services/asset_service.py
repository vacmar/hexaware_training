from sqlalchemy.orm import Session
from app.repositories.asset_repo import AssetRepository
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from fastapi import HTTPException

class AssetService:
    def __init__(self, db: Session):
        self.asset_repo = AssetRepository(db)
    
    def create_asset(self, asset_data: AssetCreate):
        existing_asset = self.asset_repo.get_asset_by_tag(asset_data.asset_tag)
        if existing_asset:
            raise HTTPException(status_code=400, detail="Asset tag already exists")
        return self.asset_repo.create_asset(asset_data)
    
    def get_asset(self, asset_id: int):
        asset = self.asset_repo.get_asset_by_id(asset_id)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    
    def get_all_assets(self, skip: int, limit: int, status: str = None, asset_type: str = None):
        return self.asset_repo.get_all_assets(skip, limit, status, asset_type)
    
    def get_department_assets(self, dept_id: int, skip: int, limit: int):
        return self.asset_repo.get_assets_by_department(dept_id, skip, limit)
    
    def update_asset(self, asset_id: int, asset_data: AssetUpdate):
        asset = self.asset_repo.update_asset(asset_id, asset_data)
        if not asset:
            raise HTTPException(status_code=404, detail="Asset not found")
        return asset
    
    def delete_asset(self, asset_id: int):
        success = self.asset_repo.delete_asset(asset_id)
        if not success:
            raise HTTPException(status_code=404, detail="Asset not found")
        return {"message": "Asset deleted successfully"}
