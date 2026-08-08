from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.database.mongodb import get_database
from app.repositories.asset_repository import AssetRepository
from app.schemas.asset import Asset, AssetCreate, AssetUpdate, AssetFilter
from app.api.dependencies.auth import get_current_active_user, require_write
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/assets", tags=["Assets"])


@router.post("/", response_model=Asset, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create a new asset."""
    asset_repo = AssetRepository(db)
    asset = await asset_repo.create(asset_data)
    return Asset(**asset)


@router.get("/", response_model=List[Asset])
async def list_assets(
    asset_type: str = None,
    criticality: str = None,
    status: str = None,
    owner: str = None,
    department: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """List assets with filtering."""
    from app.schemas.common import AssetType, Criticality
    
    asset_repo = AssetRepository(db)
    filter_obj = AssetFilter()
    
    if asset_type:
        try:
            filter_obj.asset_type = AssetType(asset_type)
        except:
            pass
    if criticality:
        try:
            filter_obj.criticality = Criticality(criticality)
        except:
            pass
    if status:
        filter_obj.status = status
    if owner:
        filter_obj.owner = owner
    if department:
        filter_obj.department = department
    
    assets = await asset_repo.list_assets(filter_obj, skip=skip, limit=limit)
    return [Asset(**asset) for asset in assets]


@router.get("/{asset_id}", response_model=Asset)
async def get_asset(
    asset_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get asset by ID."""
    asset_repo = AssetRepository(db)
    asset = await asset_repo.get_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return Asset(**asset)


@router.patch("/{asset_id}", response_model=Asset)
async def update_asset(
    asset_id: str,
    asset_data: AssetUpdate,
    current_user: dict = Depends(require_write),
    db = Depends(get_database)
):
    """Update asset."""
    asset_repo = AssetRepository(db)
    updated_asset = await asset_repo.update(asset_id, asset_data)
    if not updated_asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return Asset(**updated_asset)
