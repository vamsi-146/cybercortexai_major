from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.database.mongodb import get_database
from app.repositories.event_repository import EventRepository
from app.schemas.event import SecurityEvent, SecurityEventCreate, EventFilter
from app.api.dependencies.auth import get_current_active_user, require_write
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=SecurityEvent, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: SecurityEventCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create a new security event."""
    event_repo = EventRepository(db)
    event = await event_repo.create(event_data)
    return SecurityEvent(**event)


@router.post("/bulk", response_model=List[SecurityEvent])
async def create_events_bulk(
    events: List[SecurityEventCreate],
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create multiple security events in bulk."""
    event_repo = EventRepository(db)
    created_events = await event_repo.create_bulk(events)
    return [SecurityEvent(**event) for event in created_events]


@router.get("/", response_model=List[SecurityEvent])
async def list_events(
    source_type: str = None,
    severity: str = None,
    event_type: str = None,
    src_ip: str = None,
    dst_ip: str = None,
    username: str = None,
    hostname: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """List security events with filtering."""
    from app.schemas.common import SourceType, Severity
    
    event_repo = EventRepository(db)
    filter_obj = EventFilter()
    
    if source_type:
        try:
            filter_obj.source_type = SourceType(source_type)
        except:
            pass
    if severity:
        try:
            filter_obj.severity = Severity(severity)
        except:
            pass
    if event_type:
        filter_obj.event_type = event_type
    if src_ip:
        filter_obj.src_ip = src_ip
    if dst_ip:
        filter_obj.dst_ip = dst_ip
    if username:
        filter_obj.username = username
    if hostname:
        filter_obj.hostname = hostname
    
    events = await event_repo.list_events(filter_obj, skip=skip, limit=limit)
    return [SecurityEvent(**event) for event in events]


@router.get("/{event_id}", response_model=SecurityEvent)
async def get_event(
    event_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get event by ID."""
    event_repo = EventRepository(db)
    event = await event_repo.get_by_id(event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return SecurityEvent(**event)
