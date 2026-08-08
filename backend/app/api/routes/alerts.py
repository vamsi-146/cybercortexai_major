from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from app.database.mongodb import get_database
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import Alert, AlertCreate, AlertUpdate, AlertFilter
from app.api.dependencies.auth import get_current_active_user, require_write
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/alerts", tags=["Alerts"])


@router.post("/", response_model=Alert, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert_data: AlertCreate,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Create a new alert."""
    alert_repo = AlertRepository(db)
    alert = await alert_repo.create(alert_data)
    return Alert(**alert)


@router.get("/", response_model=List[Alert])
async def list_alerts(
    severity: str = None,
    status: str = None,
    source: str = None,
    assigned_to: str = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """List alerts with filtering."""
    from app.schemas.common import Severity, AlertStatus
    
    alert_repo = AlertRepository(db)
    filter_obj = AlertFilter()
    
    if severity:
        try:
            filter_obj.severity = Severity(severity)
        except:
            pass
    if status:
        try:
            filter_obj.status = AlertStatus(status)
        except:
            pass
    if source:
        filter_obj.source = source
    if assigned_to:
        filter_obj.assigned_to = assigned_to
    
    alerts = await alert_repo.list_alerts(filter_obj, skip=skip, limit=limit)
    return [Alert(**alert) for alert in alerts]


@router.get("/{alert_id}", response_model=Alert)
async def get_alert(
    alert_id: str,
    current_user: dict = Depends(get_current_active_user),
    db = Depends(get_database)
):
    """Get alert by ID."""
    alert_repo = AlertRepository(db)
    alert = await alert_repo.get_by_id(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return Alert(**alert)


@router.patch("/{alert_id}", response_model=Alert)
async def update_alert(
    alert_id: str,
    alert_data: AlertUpdate,
    current_user: dict = Depends(require_write),
    db = Depends(get_database)
):
    """Update alert."""
    alert_repo = AlertRepository(db)
    updated_alert = await alert_repo.update(alert_id, alert_data)
    if not updated_alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return Alert(**updated_alert)
