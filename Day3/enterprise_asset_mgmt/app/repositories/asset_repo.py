from sqlalchemy.orm import Session
from app.models.asset import Asset
from app.schemas.asset_schema import AssetCreate, AssetUpdate
from typing import Optional, List

class AssetRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_asset(self, asset_data: AssetCreate) -> Asset:
        asset = Asset(**asset_data.model_dump())
        self.db.add(asset)
        self.db.commit()
        self.db.refresh(asset)
        return asset
    
    def get_asset_by_id(self, asset_id: int) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.id == asset_id, Asset.is_deleted == False).first()
    
    def get_asset_by_tag(self, asset_tag: str) -> Optional[Asset]:
        return self.db.query(Asset).filter(Asset.asset_tag == asset_tag, Asset.is_deleted == False).first()
    
    def get_all_assets(self, skip: int = 0, limit: int = 10, status: Optional[str] = None, asset_type: Optional[str] = None) -> tuple[List[Asset], int]:
        query = self.db.query(Asset).filter(Asset.is_deleted == False)
        if status:
            query = query.filter(Asset.status == status)
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        total = query.count()
        assets = query.offset(skip).limit(limit).all()
        return assets, total
    
    def get_assets_by_department(self, dept_id: int, skip: int = 0, limit: int = 10) -> tuple[List[Asset], int]:
        query = self.db.query(Asset).filter(Asset.department_id == dept_id, Asset.is_deleted == False)
        total = query.count()
        assets = query.offset(skip).limit(limit).all()
        return assets, total
    
    def update_asset(self, asset_id: int, asset_data: AssetUpdate) -> Optional[Asset]:
        asset = self.get_asset_by_id(asset_id)
        if asset:
            for key, value in asset_data.model_dump(exclude_unset=True).items():
                setattr(asset, key, value)
            self.db.commit()
            self.db.refresh(asset)
        return asset
    
    def delete_asset(self, asset_id: int) -> bool:
        asset = self.get_asset_by_id(asset_id)
        if asset:
            asset.is_deleted = True
            self.db.commit()
            return True
        return False