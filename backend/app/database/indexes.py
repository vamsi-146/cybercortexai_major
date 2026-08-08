from app.database.mongodb import get_database
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)


async def create_indexes():
    """Create MongoDB indexes for all collections."""
    db = await get_database()
    
    # Users collection indexes
    await db.users.create_index([("email", 1)], unique=True)
    await db.users.create_index([("username", 1)], unique=True)
    await db.users.create_index([("role", 1)])
    await db.users.create_index([("is_active", 1)])
    await db.users.create_index([("created_at", -1)])
    logger.info("Created indexes for users collection")
    
    # Security events indexes
    await db.security_events.create_index([("event_id", 1)], unique=True)
    await db.security_events.create_index([("timestamp", -1)])
    await db.security_events.create_index([("source_type", 1)])
    await db.security_events.create_index([("source_name", 1)])
    await db.security_events.create_index([("event_type", 1)])
    await db.security_events.create_index([("severity", 1)])
    await db.security_events.create_index([("category", 1)])
    await db.security_events.create_index([("username", 1)])
    await db.security_events.create_index([("src_ip", 1)])
    await db.security_events.create_index([("dst_ip", 1)])
    await db.security_events.create_index([("hostname", 1)])
    await db.security_events.create_index([("device_id", 1)])
    await db.security_events.create_index([("timestamp", -1), ("username", 1)])
    await db.security_events.create_index([("timestamp", -1), ("src_ip", 1)])
    await db.security_events.create_index([("timestamp", -1), ("dst_ip", 1)])
    await db.security_events.create_index([("timestamp", -1), ("hostname", 1)])
    await db.security_events.create_index([("mitre_techniques", 1)])
    # TTL index for 90 days
    await db.security_events.create_index([("created_at", 1)], expireAfterSeconds=90*24*3600)
    logger.info("Created indexes for security_events collection")
    
    # Alerts indexes
    await db.alerts.create_index([("alert_id", 1)], unique=True)
    await db.alerts.create_index([("severity", 1)])
    await db.alerts.create_index([("status", 1)])
    await db.alerts.create_index([("source", 1)])
    await db.alerts.create_index([("created_at", -1)])
    await db.alerts.create_index([("assigned_to", 1)])
    await db.alerts.create_index([("incident_id", 1)])
    await db.alerts.create_index([("status", 1), ("severity", 1)])
    await db.alerts.create_index([("created_at", -1), ("severity", 1)])
    logger.info("Created indexes for alerts collection")
    
    # Incidents indexes
    await db.incidents.create_index([("incident_id", 1)], unique=True)
    await db.incidents.create_index([("severity", 1)])
    await db.incidents.create_index([("status", 1)])
    await db.incidents.create_index([("assigned_to", 1)])
    await db.incidents.create_index([("created_at", -1)])
    await db.incidents.create_index([("status", 1), ("created_at", -1)])
    logger.info("Created indexes for incidents collection")
    
    # Assets indexes
    await db.assets.create_index([("asset_id", 1)], unique=True)
    await db.assets.create_index([("hostname", 1)])
    await db.assets.create_index([("criticality", 1)])
    await db.assets.create_index([("asset_type", 1)])
    logger.info("Created indexes for assets collection")
    
    # Data sources indexes
    await db.data_sources.create_index([("source_id", 1)], unique=True)
    await db.data_sources.create_index([("type", 1)])
    await db.data_sources.create_index([("enabled", 1)])
    logger.info("Created indexes for data_sources collection")
    
    # Audit logs indexes
    await db.audit_logs.create_index([("timestamp", -1)])
    await db.audit_logs.create_index([("user_id", 1)])
    await db.audit_logs.create_index([("action", 1)])
    await db.audit_logs.create_index([("resource_type", 1)])
    await db.audit_logs.create_index([("resource_id", 1)])
    await db.audit_logs.create_index([("user_id", 1), ("timestamp", -1)])
    # TTL index for 365 days
    await db.audit_logs.create_index([("created_at", 1)], expireAfterSeconds=365*24*3600)
    logger.info("Created indexes for audit_logs collection")
    
    logger.info("All database indexes created successfully")


if __name__ == "__main__":
    import asyncio
    asyncio.run(create_indexes())
