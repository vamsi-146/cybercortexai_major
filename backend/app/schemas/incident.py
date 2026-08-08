from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime
from .common import Severity, IncidentStatus, Criticality


class AffectedAsset(BaseModel):
    type: str  # USER, DEVICE, HOST, APPLICATION, DATABASE
    id: str
    name: str
    criticality: Criticality


class TimelineEvent(BaseModel):
    timestamp: datetime
    event: str
    description: str
    severity: Optional[Severity] = None


class RiskFactor(BaseModel):
    factor: str
    impact: float = Field(..., ge=0, le=1)
    description: str


class RiskAssessment(BaseModel):
    overall_score: int = Field(..., ge=0, le=100)
    factors: List[RiskFactor]


class IncidentCreate(BaseModel):
    incident_id: str = Field(..., min_length=1)
    title: str
    description: str
    severity: Severity
    affected_assets: List[AffectedAsset] = []
    mitre_techniques: Optional[List[str]] = []
    indicators: Optional[List[Dict[str, Any]]] = []
    recommended_actions: Optional[List[str]] = []


class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    assigned_to: Optional[str] = None
    timeline: Optional[List[TimelineEvent]] = None
    recommended_actions: Optional[List[str]] = None


class Incident(BaseModel):
    id: str
    incident_id: str
    title: str
    description: str
    severity: Severity
    status: IncidentStatus
    risk_score: int = Field(..., ge=0, le=100)
    alert_ids: List[str] = []
    event_ids: List[str] = []
    affected_assets: List[AffectedAsset] = []
    affected_users: List[str] = []
    indicators: List[Dict[str, Any]] = []
    mitre_techniques: List[str] = []
    assigned_to: Optional[str] = None
    timeline: List[TimelineEvent] = []
    tags: List[str] = []
    recommendations: List[str] = []
    created_at: datetime
    updated_at: datetime
    closed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class IncidentDetail(Incident):
    """Extended incident detail with additional fields."""
    risk_assessment: Optional[RiskAssessment] = None
    investigation_id: Optional[str] = None
    related_alerts: List[str] = []


class IncidentFilter(BaseModel):
    severity: Optional[Severity] = None
    status: Optional[IncidentStatus] = None
    assigned_to: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    search: Optional[str] = None
