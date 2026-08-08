from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.asset import AssetCreate, AssetUpdate, AssetFilter
import logging

logger = logging.getLogger(__name__)


class AssetRepository:
    """Repository for asset operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.assets

    async def create(self, asset_data: AssetCreate) -> dict:
        """Create a new asset."""
        asset_dict = asset_data.model_dump()
        asset_dict["risk_score"] = 0
        asset_dict["vulnerabilities"] = []
        asset_dict["first_seen"] = datetime.utcnow()
        asset_dict["last_seen"] = datetime.utcnow()
        asset_dict["status"] = "ACTIVE"
        asset_dict["created_at"] = datetime.utcnow()
        asset_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(asset_dict)
        asset_dict["_id"] = str(result.inserted_id)
        asset_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created asset: {asset_dict['asset_id']}")
        return asset_dict

    async def get_by_asset_id(self, asset_id: str) -> Optional[dict]:
        """Get asset by asset_id."""
        return await self.collection.find_one({"asset_id": asset_id})

    async def get_by_id(self, asset_id: str) -> Optional[dict]:
        """Get asset by MongoDB ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(asset_id)})
        except:
            return None

    async def update(self, asset_id: str, asset_data: AssetUpdate) -> Optional[dict]:
        """Update asset."""
        update_dict = asset_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        try:
            await self.collection.update_one(
                {"_id": ObjectId(asset_id)},
                {"$set": update_dict}
            )
            return await self.get_by_id(asset_id)
        except:
            return None

    async def list_assets(
        self, 
        filter: AssetFilter, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """List assets with filtering and pagination."""
        query = self._build_filter_query(filter)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        assets = await cursor.to_list(length=limit)
        for asset in assets:
            asset["id"] = str(asset["_id"])
        return assets

    async def count_assets(self, filter: AssetFilter) -> int:
        """Count assets matching filter."""
        query = self._build_filter_query(filter)
        return await self.collection.count_documents(query)

    def _build_filter_query(self, filter: AssetFilter) -> dict:
        """Build MongoDB query from filter."""
        query = {}
        if filter.asset_type:
            query["asset_type"] = filter.asset_type.value
        if filter.criticality:
            query["criticality"] = filter.criticality.value
        if filter.status:
            query["status"] = filter.status
        if filter.owner:
            query["owner"] = filter.owner
        if filter.department:
            query["department"] = filter.department
        return query

    async def get_count_by_criticality(self) -> List[dict]:
        """Get asset count grouped by criticality."""
        pipeline = [
            {"$group": {"_id": "$criticality", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=100)

    async def count_assets(self, filter: AssetFilter = None) -> int:
        """Count all assets or assets matching filter."""
        query = self._build_filter_query(filter) if filter else {}
        return await self.collection.count_documents(query)
