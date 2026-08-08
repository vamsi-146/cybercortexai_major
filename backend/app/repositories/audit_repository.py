from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.audit import AuditLogCreate
import logging

logger = logging.getLogger(__name__)


class AuditLogRepository:
    """Repository for audit log operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.audit_logs

    async def create(self, audit_data: AuditLogCreate) -> dict:
        """Create a new audit log entry."""
        audit_dict = audit_data.model_dump()
        audit_dict["timestamp"] = datetime.utcnow()
        audit_dict["created_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(audit_dict)
        audit_dict["_id"] = str(result.inserted_id)
        audit_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created audit log: {audit_dict['action']} on {audit_dict['resource_type']}")
        return audit_dict

    async def list_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """List audit logs for a specific user."""
        cursor = self.collection.find({"user_id": user_id}).sort("timestamp", -1).skip(skip).limit(limit)
        logs = await cursor.to_list(length=limit)
        for log in logs:
            log["id"] = str(log["_id"])
        return logs

    async def list_by_resource(self, resource_type: str, resource_id: str, skip: int = 0, limit: int = 100) -> List[dict]:
        """List audit logs for a specific resource."""
        cursor = self.collection.find({
            "resource_type": resource_type,
            "resource_id": resource_id
        }).sort("timestamp", -1).skip(skip).limit(limit)
        logs = await cursor.to_list(length=limit)
        for log in logs:
            log["id"] = str(log["_id"])
        return logs
