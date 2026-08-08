from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.database.mongodb import get_database
from app.repositories.datasource_repository import DataSourceRepository
from app.schemas.datasource import DataSource, DataSourceCreate, DataSourceUpdate, DataSourceFilter
from app.api.dependencies.auth import get_current_active_user, require_admin
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/data-sources", tags=["Data Sources"])


@router.post("/", response_model=DataSource, status_code=status.HTTP_201_CREATED)
async def create_datasource(
    datasource_data: DataSourceCreate,
    current_user: dict = Depends(require_admin),
    db = Depends(get_database)
):
    """Create a new data source (admin only)."""
    ds_repo = DataSourceRepository(db)
    datasource = await ds_repo.create(datasource_data)
    return DataSource(**datasource)


@router.get("/", response_model=List[DataSource])
async def list_datasources(
    type: str = None,
    enabled: bool = None,
    status: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """List data sources with filtering."""
    from app.schemas.common import SourceType
    
    ds_repo = DataSourceRepository(db)
    filter_obj = DataSourceFilter()
    
    if type:
        try:
            filter_obj.type = SourceType(type)
        except:
            pass
    if enabled is not None:
        filter_obj.enabled = enabled
    if status:
        filter_obj.status = status
    
    datasources = await ds_repo.list_datasources(filter_obj, skip=skip, limit=limit)
    return [DataSource(**ds) for ds in datasources]


@router.get("/{source_id}", response_model=DataSource)
async def get_datasource(
    source_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get data source by ID."""
    ds_repo = DataSourceRepository(db)
    datasource = await ds_repo.get_by_id(source_id)
    if not datasource:
        raise HTTPException(status_code=404, detail="Data source not found")
    return DataSource(**datasource)


@router.patch("/{source_id}", response_model=DataSource)
async def update_datasource(
    source_id: str,
    datasource_data: DataSourceUpdate,
    current_user: dict = Depends(require_admin),
    db = Depends(get_database)
):
    """Update data source (admin only)."""
    ds_repo = DataSourceRepository(db)
    updated_datasource = await ds_repo.update(source_id, datasource_data)
    if not updated_datasource:
        raise HTTPException(status_code=404, detail="Data source not found")
    return DataSource(**updated_datasource)
