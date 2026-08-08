from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.database.mongodb import get_database
from app.repositories.user_repository import UserRepository
from app.schemas.user import User, UserUpdate
from app.api.dependencies.auth import get_current_active_user, require_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=User)
async def get_me(current_user: dict = Depends(get_current_active_user)):
    """Get current user information."""
    return User(**current_user)


@router.get("/", response_model=List[User])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    current_user: dict = Depends(require_admin),
    db = Depends(get_database)
):
    """List all users (admin only)."""
    user_repo = UserRepository(db)
    users = await user_repo.list_users(skip=skip, limit=limit)
    return [User(**user) for user in users]


@router.patch("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: dict = Depends(require_admin),
    db = Depends(get_database)
):
    """Update user (admin only)."""
    user_repo = UserRepository(db)
    updated_user = await user_repo.update(user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return User(**updated_user)
