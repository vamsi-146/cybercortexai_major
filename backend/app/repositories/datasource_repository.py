from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.datasource import DataSourceCreate, DataSourceUpdate, DataSourceFilter
import logging

logger = logging.getLogger(__name__)


class DataSourceRepository:
    """Repository for data source operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.data_sources

    async def create(self, datasource_data: DataSourceCreate) -> dict:
        """Create a new data source."""
        ds_dict = datasource_data.model_dump()
        ds_dict["status"] = "ENABLED" if ds_dict.get("enabled") else "DISABLED"
        ds_dict["event_count"] = 0
        ds_dict["created_at"] = datetime.utcnow()
        ds_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(ds_dict)
        ds_dict["_id"] = str(result.inserted_id)
        ds_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created data source: {ds_dict['source_id']}")
        return ds_dict

    async def get_by_source_id(self, source_id: str) -> Optional[dict]:
        """Get data source by source_id."""
        return await self.collection.find_one({"source_id": source_id})

    async def get_by_id(self, source_id: str) -> Optional[dict]:
        """Get data source by MongoDB ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(source_id)})
        except:
            return None

    async def update(self, source_id: str, datasource_data: DataSourceUpdate) -> Optional[dict]:
        """Update data source."""
        update_dict = datasource_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        if "enabled" in update_dict:
            update_dict["status"] = "ENABLED" if update_dict["enabled"] else "DISABLED"
        
        try:
            await self.collection.update_one(
                {"_id": ObjectId(source_id)},
                {"$set": update_dict}
            )
            return await self.get_by_id(source_id)
        except:
            return None

    async def list_datasources(
        self, 
        filter: DataSourceFilter, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """List data sources with filtering and pagination."""
        query = self._build_filter_query(filter)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        datasources = await cursor.to_list(length=limit)
        for ds in datasources:
            ds["id"] = str(ds["_id"])
        return datasources

    def _build_filter_query(self, filter: DataSourceFilter) -> dict:
        """Build MongoDB query from filter."""
        query = {}
        if filter.type:
            query["type"] = filter.type.value
        if filter.enabled is not None:
            query["enabled"] = filter.enabled
        if filter.status:
            query["status"] = filter.status
        return query

    async def update_event_count(self, source_id: str) -> None:
        """Increment event count for a data source."""
        try:
            await self.collection.update_one(
                {"source_id": source_id},
                {"$inc": {"event_count": 1}, "$set": {"last_event_at": datetime.utcnow()}}
            )
        except:
            pass
