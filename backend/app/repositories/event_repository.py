from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.event import SecurityEventCreate, EventFilter
import logging

logger = logging.getLogger(__name__)


class EventRepository:
    """Repository for security event operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.security_events

    async def create(self, event_data: SecurityEventCreate) -> dict:
        """Create a new security event."""
        event_dict = event_data.model_dump()
        if not event_dict.get("received_at"):
            event_dict["received_at"] = datetime.utcnow()
        event_dict["created_at"] = datetime.utcnow()
        event_dict["processed"] = False
        
        result = await self.collection.insert_one(event_dict)
        event_dict["_id"] = str(result.inserted_id)
        event_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created event: {event_dict['event_id']}")
        return event_dict

    async def create_bulk(self, events: List[SecurityEventCreate]) -> List[dict]:
        """Create multiple security events."""
        event_dicts = []
        for event in events:
            event_dict = event.model_dump()
            if not event_dict.get("received_at"):
                event_dict["received_at"] = datetime.utcnow()
            event_dict["created_at"] = datetime.utcnow()
            event_dict["processed"] = False
            event_dicts.append(event_dict)
        
        if event_dicts:
            result = await self.collection.insert_many(event_dicts)
            for i, event_dict in enumerate(event_dicts):
                event_dict["_id"] = str(result.inserted_ids[i])
                event_dict["id"] = str(result.inserted_ids[i])
        
        logger.info(f"Created {len(event_dicts)} events in bulk")
        return event_dicts

    async def get_by_event_id(self, event_id: str) -> Optional[dict]:
        """Get event by event_id."""
        return await self.collection.find_one({"event_id": event_id})

    async def get_by_id(self, event_id: str) -> Optional[dict]:
        """Get event by MongoDB ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(event_id)})
        except:
            return None

    async def list_events(
        self, 
        filter: EventFilter, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[dict]:
        """List events with filtering and pagination."""
        query = self._build_filter_query(filter)
        cursor = self.collection.find(query).skip(skip).limit(limit)
        events = await cursor.to_list(length=limit)
        for event in events:
            event["id"] = str(event["_id"])
        return events

    async def count_events(self, filter: EventFilter) -> int:
        """Count events matching filter."""
        query = self._build_filter_query(filter)
        return await self.collection.count_documents(query)

    def _build_filter_query(self, filter: EventFilter) -> dict:
        """Build MongoDB query from filter."""
        query = {}
        if filter.source_type:
            query["source_type"] = filter.source_type.value
        if filter.severity:
            query["normalized_event.severity"] = filter.severity.value
        if filter.event_type:
            query["normalized_event.event_type"] = filter.event_type
        if filter.src_ip:
            query["normalized_event.source_ip"] = filter.src_ip
        if filter.dst_ip:
            query["normalized_event.destination_ip"] = filter.dst_ip
        if filter.username:
            query["normalized_event.user"] = filter.username
        if filter.hostname:
            query["normalized_event.host"] = filter.hostname
        if filter.start_time or filter.end_time:
            query["normalized_event.timestamp"] = {}
            if filter.start_time:
                query["normalized_event.timestamp"]["$gte"] = filter.start_time
            if filter.end_time:
                query["normalized_event.timestamp"]["$lte"] = filter.end_time
        return query

    async def mark_processed(self, event_id: str) -> None:
        """Mark event as processed."""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(event_id)},
                {"$set": {"processed": True}}
            )
        except:
            pass

    async def get_count_by_source(self) -> List[dict]:
        """Get event count grouped by source."""
        pipeline = [
            {"$group": {"_id": "$source", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=100)

    async def get_count_by_severity(self) -> List[dict]:
        """Get event count grouped by severity."""
        pipeline = [
            {"$group": {"_id": "$normalized_event.severity", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        cursor = self.collection.aggregate(pipeline)
        return await cursor.to_list(length=100)
