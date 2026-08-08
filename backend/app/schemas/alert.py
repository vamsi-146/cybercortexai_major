from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .common import Severity, AlertStatus


class Indicator(BaseModel):
    type: str  # IP, DOMAIN, HASH, EMAIL, URL
    value: str
    confidence: float = Field(..., ge=0, le=1)


class AlertCreate(BaseModel):
    alert_id: str = Field(..., min_length=1)
    title: str
    description: str
    severity: Severity
    source: str
    rule_id: Optional[str] = None
    confidence_score: Optional[float] = Field(None, ge=0, le=100)
    mitre_techniques: Optional[List[str]] = []
    iocs: Optional[List[Indicator]] = []
    related_event_ids: Optional[List[str]] = []


class AlertUpdate(BaseModel):
    status: Optional[AlertStatus] = None
    assigned_to: Optional[str] = None
    resolution_notes: Optional[str] = None


class Alert(BaseModel):
    id: str
    alert_id: str
    title: str
    description: str
    severity: Severity
    status: AlertStatus
    source: str
    rule_id: Optional[str] = None
    confidence_score: Optional[float] = None
    mitre_techniques: List[str] = []
    iocs: List[Indicator] = []
    related_event_ids: List[str] = []
    assigned_to: Optional[str] = None
    incident_id: Optional[str] = None
    first_seen: datetime
    last_seen: datetime
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None
    resolution_notes: Optional[str] = None

    class Config:
        from_attributes = True


class AlertFilter(BaseModel):
    severity: Optional[Severity] = None
    status: Optional[AlertStatus] = None
    source: Optional[str] = None
    assigned_to: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
