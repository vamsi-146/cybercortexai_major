from typing import Optional, List
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from datetime import datetime
from app.schemas.user import UserCreate, UserUpdate, Role
from app.core.security import get_password_hash, verify_password
import logging

logger = logging.getLogger(__name__)


class UserRepository:
    """Repository for user operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db.users

    async def create(self, user_data: UserCreate) -> dict:
        """Create a new user."""
        user_dict = user_data.model_dump()
        user_dict["password_hash"] = get_password_hash(user_dict.pop("password"))
        user_dict["is_active"] = True
        user_dict["created_at"] = datetime.utcnow()
        user_dict["updated_at"] = datetime.utcnow()
        
        result = await self.collection.insert_one(user_dict)
        user_dict["_id"] = str(result.inserted_id)
        user_dict["id"] = str(result.inserted_id)
        
        logger.info(f"Created user: {user_dict['email']}")
        return user_dict

    async def get_by_email(self, email: str) -> Optional[dict]:
        """Get user by email."""
        return await self.collection.find_one({"email": email})

    async def get_by_username(self, username: str) -> Optional[dict]:
        """Get user by username."""
        return await self.collection.find_one({"username": username})

    async def get_by_id(self, user_id: str) -> Optional[dict]:
        """Get user by ID."""
        try:
            return await self.collection.find_one({"_id": ObjectId(user_id)})
        except:
            return None

    async def update(self, user_id: str, user_data: UserUpdate) -> Optional[dict]:
        """Update user."""
        update_dict = user_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = datetime.utcnow()
        
        try:
            await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": update_dict}
            )
            return await self.get_by_id(user_id)
        except:
            return None

    async def update_last_login(self, user_id: str) -> None:
        """Update user's last login timestamp."""
        try:
            await self.collection.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"last_login": datetime.utcnow()}}
            )
        except:
            pass

    async def list_users(self, skip: int = 0, limit: int = 100) -> List[dict]:
        """List all users with pagination."""
        cursor = self.collection.find().skip(skip).limit(limit)
        users = await cursor.to_list(length=limit)
        for user in users:
            user["id"] = str(user["_id"])
        return users

    async def delete(self, user_id: str) -> bool:
        """Delete user."""
        try:
            result = await self.collection.delete_one({"_id": ObjectId(user_id)})
            return result.deleted_count > 0
        except:
            return False
