from fastapi import APIRouter, Depends
from app.database.mongodb import get_database
from app.repositories.event_repository import EventRepository
from app.repositories.alert_repository import AlertRepository
from app.repositories.incident_repository import IncidentRepository
from app.repositories.asset_repository import AssetRepository
from app.schemas.dashboard import DashboardOverview, KPIMetric, SeverityDistribution, EventSource, SystemService, MITRETrend
from app.api.dependencies.auth import get_current_active_user
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get("/overview", response_model=DashboardOverview)
async def get_dashboard_overview(current_user: dict = Depends(get_current_active_user), db = Depends(get_database)):
    """Get dashboard overview data."""
    event_repo = EventRepository(db)
    alert_repo = AlertRepository(db)
    incident_repo = IncidentRepository(db)
    asset_repo = AssetRepository(db)

    # Calculate time ranges
    now = datetime.utcnow()
    yesterday = now - timedelta(days=1)

    # Get counts
    active_threats_count = await incident_repo.count_incidents(filter=None)
    critical_incidents_count = await incident_repo.count_incidents(filter={"severity": "critical"})
    events_analyzed_count = await event_repo.count_events(filter=None)
    correlated_alerts_count = await alert_repo.count_alerts(filter=None)

    # Get severity distribution for incidents
    severity_dist = await incident_repo.get_count_by_severity()
    severity_distribution = []
    total_severity = sum(item["count"] for item in severity_dist) if severity_dist else 1

    for item in severity_dist:
        severity_distribution.append(SeverityDistribution(
            severity=item["_id"],
            count=item["count"],
            percentage=round((item["count"] / total_severity) * 100, 1)
        ))

    # Get events by source
    events_by_source_data = await event_repo.get_count_by_source()
    total_source = sum(item["count"] for item in events_by_source_data) if events_by_source_data else 1

    event_sources = []
    for item in events_by_source_data[:7]:  # Top 7 sources
        event_sources.append(EventSource(
            name=item["_id"],
            count=item["count"],
            percentage=round((item["count"] / total_source) * 100, 1)
        ))

    # Get recent incidents
    recent_incidents = await incident_repo.get_recent(limit=6)

    # Get top MITRE techniques from incidents
    mitre_data = await incident_repo.get_mitre_techniques()
    mitre_trends = []
    for item in mitre_data[:5]:  # Top 5
        mitre_trends.append(MITRETrend(
            technique=item["_id"],
            count=item["count"]
        ))

    # System health
    from app.database.mongodb import MongoDB
    mongo_healthy = await MongoDB.health_check()

    system_health = [
        SystemService(name="API", status="OPERATIONAL", available=True),
        SystemService(name="MongoDB", status="OPERATIONAL" if mongo_healthy else "UNAVAILABLE", available=mongo_healthy),
        SystemService(name="Agent Engine", status="UNAVAILABLE", available=False),  # Phase 5
        SystemService(name="Neo4j", status="UNAVAILABLE", available=False),  # Phase 7
        SystemService(name="Prediction Engine", status="UNAVAILABLE", available=False),  # Phase 9
    ]

    # Build KPIs
    return DashboardOverview(
        active_threats=KPIMetric(
            id="active-threats",
            label="Active Threats",
            value=active_threats_count,
            trend=0,
            available=True
        ),
        critical_incidents=KPIMetric(
            id="critical-incidents",
            label="Critical Incidents",
            value=critical_incidents_count,
            trend=0,
            available=True
        ),
        events_analyzed=KPIMetric(
            id="events-analyzed",
            label="Events Analyzed",
            value=events_analyzed_count,
            trend=0,
            available=True
        ),
        ai_investigations=KPIMetric(
            id="ai-investigations",
            label="AI Investigations",
            value=0,
            trend=0,
            available=False  # Phase 5
        ),
        correlated_alerts=KPIMetric(
            id="correlated-alerts",
            label="Correlated Alerts",
            value=correlated_alerts_count,
            trend=0,
            available=True
        ),
        high_risk_assets=KPIMetric(
            id="high-risk-assets",
            label="High-Risk Assets",
            value=await asset_repo.count_assets(filter={"criticality": "high"}),
            trend=0,
            available=True
        ),
        severity_distribution=severity_distribution,
        events_by_source=event_sources,
        recent_incidents=recent_incidents,
        mitre_trends=mitre_trends,
        system_health=system_health
    )
