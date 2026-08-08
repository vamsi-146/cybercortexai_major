from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)


class MongoDB:
    """MongoDB client wrapper for managing database connections."""

    client: Optional[AsyncIOMotorClient] = None
    database = None

    @classmethod
    async def connect(cls) -> None:
        """Establish connection to MongoDB."""
        settings = get_settings()
        
        try:
            cls.client = AsyncIOMotorClient(settings.mongodb_connection_string)
            cls.database = cls.client[settings.MONGODB_DATABASE]
            
            # Verify connection
            await cls.client.admin.command('ping')
            logger.info(f"Connected to MongoDB: {settings.MONGODB_DATABASE}")
        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise

    @classmethod
    async def close(cls) -> None:
        """Close MongoDB connection."""
        if cls.client:
            cls.client.close()
            logger.info("MongoDB connection closed")

    @classmethod
    def get_database(cls):
        """Get database instance."""
        if cls.database is None:
            raise RuntimeError("Database not initialized. Call connect() first.")
        return cls.database

    @classmethod
    async def health_check(cls) -> bool:
        """Check if MongoDB connection is healthy."""
        try:
            if cls.client:
                await cls.client.admin.command('ping')
                return True
            return False
        except Exception as e:
            logger.error(f"MongoDB health check failed: {e}")
            return False


async def get_database():
    """Dependency function to get database instance."""
    return MongoDB.get_database()
