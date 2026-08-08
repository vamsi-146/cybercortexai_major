from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.database.mongodb import get_database
from app.repositories.incident_repository import IncidentRepository
from app.schemas.incident import Incident, IncidentCreate, IncidentUpdate, IncidentFilter
from app.api.dependencies.auth import get_current_active_user, require_write
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.post("/", response_model=Incident, status_code=status.HTTP_201_CREATED)
async def create_incident(
    incident_data: IncidentCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create a new incident."""
    incident_repo = IncidentRepository(db)
    incident = await incident_repo.create(incident_data)
    return Incident(**incident)


@router.get("/", response_model=List[Incident])
async def list_incidents(
    severity: str = None,
    status: str = None,
    assigned_to: str = None,
    search: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """List incidents with filtering."""
    from app.schemas.common import Severity, IncidentStatus
    
    incident_repo = IncidentRepository(db)
    filter_obj = IncidentFilter()
    
    if severity:
        try:
            filter_obj.severity = Severity(severity)
        except:
            pass
    if status:
        try:
            filter_obj.status = IncidentStatus(status)
        except:
            pass
    if assigned_to:
        filter_obj.assigned_to = assigned_to
    if search:
        filter_obj.search = search
    
    incidents = await incident_repo.list_incidents(filter_obj, skip=skip, limit=limit)
    return [Incident(**incident) for incident in incidents]


@router.get("/{incident_id}", response_model=Incident)
async def get_incident(
    incident_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get incident by ID."""
    incident_repo = IncidentRepository(db)
    incident = await incident_repo.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return Incident(**incident)


@router.patch("/{incident_id}", response_model=Incident)
async def update_incident(
    incident_id: str,
    incident_data: IncidentUpdate,
    current_user: dict = Depends(require_write),
    db = Depends(get_database)
):
    """Update incident."""
    incident_repo = IncidentRepository(db)
    updated_incident = await incident_repo.update(incident_id, incident_data)
    if not updated_incident:
        raise HTTPException(status_code=404, detail="Incident not found")
    return Incident(**updated_incident)
