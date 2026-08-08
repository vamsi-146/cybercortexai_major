from pydantic import BaseModel
from typing import Optional, List
from .common import Severity


class KPIMetric(BaseModel):
    id: str
    label: str
    value: int | str
    trend: int
    previous_value: Optional[int] = None
    available: bool = True


class SeverityDistribution(BaseModel):
    severity: Severity
    count: int
    percentage: float


class EventSource(BaseModel):
    name: str
    count: int
    percentage: float


class SystemService(BaseModel):
    name: str
    status: str  # OPERATIONAL, DEGRADED, UNAVAILABLE
    latency: Optional[int] = None
    uptime: Optional[str] = None
    available: bool = True


class MITRETrend(BaseModel):
    technique: str
    count: int


class DashboardOverview(BaseModel):
    """Dashboard aggregation response."""
    active_threats: KPIMetric
    critical_incidents: KPIMetric
    events_analyzed: KPIMetric
    ai_investigations: KPIMetric  # Will be unavailable in Phase 2
    correlated_alerts: KPIMetric
    high_risk_assets: KPIMetric
    severity_distribution: List[SeverityDistribution]
    events_by_source: List[EventSource]
    recent_incidents: List[dict]  # Simplified for Phase 2
    mitre_trends: List[MITRETrend] = []
    system_health: List[SystemService]
