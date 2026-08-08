from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.incident import IncidentCreate, IncidentUpdate, IncidentFilter
import logging

logger = logging.getLogger(__name__)


class IncidentRepository:
    """Repository for incident operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.incidents

    async def create(self, incident_data: IncidentCreate) -> dict:
        """Create a new incident."""
        incident_dict = incident_data.model_dump()
        incident_dict["status"] = "OPEN"
        incident_dict["risk_score"] = 50  # Default risk score
        incident_dict["alert_ids"] = []
        incident_dict["event_ids"] = []
        incident_dict["affected_users"] = []
        incident_dict["timeline"] = []
        incident_dict["tags"] = []
        incident_dict["recommendations"] = incident_dict.get("recommended_actions", [])
        if "recommended_actions" in incident_dict:
            del incident_dict["recommended_actions"]
        incident_dict["created_at"] = datetime.utcnow()
        incident_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(incident_dict)
        incident_dict["_id"] = str(result.inserted_id)
        incident_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created incident: {incident_dict['incident_id']}")
        return incident_dict

    async def get_by_incident_id(self, incident_id: str) -> Optional[dict]:
        """Get incident by incident_id."""
        return await self.collection.find_one({"incident_id": incident_id})

    async def get_by_id(self, incident_id: str) -> Optional[dict]:
        """Get incident by MongoDB ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(incident_id)})
        except:
            return None

    async def update(self, incident_id: str, incident_data: IncidentUpdate) -> Optional[dict]:
        """Update incident."""
        update_dict = incident_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        if incident_data.status == "CLOSED":
            update_dict["closed_at"] = datetime.utcnow()
        
        try:
            await self.collection.update_one(
                {"_id": ObjectId(incident_id)},
                {"$set": update_dict}
            )
            return await self.get_by_id(incident_id)
        except:
            return None

    async def list_incidents(
        self,
        filter: IncidentFilter = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[dict]:
        """List incidents with filtering and pagination."""
        query = self._build_filter_query(filter) if filter else {}
        cursor = self.collection.find(query).sort("created_at", -1).skip(skip).limit(limit)
        incidents = await cursor.to_list(length=limit)
        for incident in incidents:
            incident["id"] = str(incident["_id"])
        return incidents

    def _build_filter_query(self, filter: IncidentFilter = None) -> dict:
        """Build MongoDB query from filter."""
        query = {}
        if filter:
            if filter.severity:
                query["severity"] = filter.severity.value
            if filter.status:
                query["status"] = filter.status.value
            if filter.assigned_to:
                query["assigned_to"] = filter.assigned_to
            if filter.start_time or filter.end_time:
                query["created_at"] = {}
                if filter.start_time:
                    query["created_at"]["$gte"] = filter.start_time
                if filter.end_time:
                    query["created_at"]["$lte"] = filter.end_time
            if filter.search:
                query["$or"] = [
                    {"title": {"$regex": filter.search, "$options": "i"}},
                    {"description": {"$regex": filter.search, "$options": "i"}}
                ]
        return query

    async def get_count_by_severity(self) -> List[dict]:
        """Get incident count grouped by severity."""
        pipeline = [
            {"$group": {"_id": "$severity", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=100)

    async def get_recent(self, limit: int = 10) -> List[dict]:
        """Get recent incidents."""
        cursor = self.collection.find().sort("created_at", -1).limit(limit)
        incidents = await cursor.to_list(length=limit)
        for incident in incidents:
            incident["id"] = str(incident["_id"])
        return incidents

    async def get_mitre_techniques(self) -> List[dict]:
        """Get top MITRE techniques from incidents."""
        pipeline = [
            {"$unwind": "$mitre_techniques"},
            {"$group": {"_id": "$mitre_techniques", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 10}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=10)

    async def count_incidents(self, filter: IncidentFilter = None) -> int:
        """Count all incidents or incidents matching filter."""
        query = self._build_filter_query(filter) if filter else {}
        return await self.collection.count_documents(query)
