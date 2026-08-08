from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.alert import AlertCreate, AlertUpdate, AlertFilter
import logging

logger = logging.getLogger(__name__)


class AlertRepository:
    """Repository for alert operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.alerts

    async def create(self, alert_data: AlertCreate) -> dict:
        """Create a new alert."""
        alert_dict = alert_data.model_dump()
        alert_dict["status"] = "NEW"
        alert_dict["first_seen"] = datetime.utcnow()
        alert_dict["last_seen"] = datetime.utcnow()
        alert_dict["created_at"] = datetime.utcnow()
        alert_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(alert_dict)
        alert_dict["_id"] = str(result.inserted_id)
        alert_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created alert: {alert_dict['alert_id']}")
        return alert_dict

    async def get_by_alert_id(self, alert_id: str) -> Optional[dict]:
        """Get alert by alert_id."""
        return await self.collection.find_one({"alert_id": alert_id})

    async def get_by_id(self, alert_id: str) -> Optional[dict]:
        """Get alert by MongoDB ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(alert_id)})
        except:
            return None

    async def update(self, alert_id: str, alert_data: AlertUpdate) -> Optional[dict]:
        """Update alert."""
        update_dict = alert_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        if alert_data.status == "RESOLVED":
            update_dict["resolved_at"] = datetime.utcnow()
        
        try:
            await self.collection.update_one(
                {"_id": ObjectId(alert_id)},
                {"$set": update_dict}
            )
            return await self.get_by_id(alert_id)
        except:
            return None

    async def list_alerts(
        self, 
        filter: AlertFilter, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """List alerts with filtering and pagination."""
        query = self._build_filter_query(filter)
        cursor = self.collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        alerts = await cursor.to_list(length=limit)
        for alert in alerts:
            alert["id"] = str(alert["_id"])
        return alerts

    async def count_alerts(self, filter: AlertFilter) -> int:
        """Count alerts matching filter."""
        query = self._build_filter_query(filter)
        return await self.collection.count_documents(query)

    def _build_filter_query(self, filter: AlertFilter) -> dict:
        """Build MongoDB query from filter."""
        query = {}
        if filter.severity:
            query["severity"] = filter.severity.value
        if filter.status:
            query["status"] = filter.status.value
        if filter.source:
            query["source"] = filter.source
        if filter.assigned_to:
            query["assigned_to"] = filter.assigned_to
        if filter.start_time or filter.end_time:
            query["created_at"] = {}
            if filter.start_time:
                query["created_at"]["$gte"] = filter.start_time
            if filter.end_time:
                query["created_at"]["$lte"] = filter.end_time
        return query

    async def get_count_by_severity(self) -> List[dict]:
        """Get alert count grouped by severity."""
        pipeline = [
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=100)
