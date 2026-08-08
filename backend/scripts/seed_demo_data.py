"""
Seed script for CyberCortex development data.
Run with: python scripts/seed_demo_data.py
"""
import asyncio
import sys
from datetime import datetime, timedelta
from app.database.mongodb import MongoDB, get_database
from app.repositories.user_repository import UserRepository
from app.repositories.event_repository import EventRepository
from app.repositories.alert_repository import AlertRepository
from app.repositories.incident_repository import IncidentRepository
from app.repositories.asset_repository import AssetRepository
from app.repositories.datasource_repository import DataSourceRepository
from app.schemas.user import UserCreate, Role
from app.schemas.event import SecurityEventCreate, NormalizedEvent, SourceType, Severity
from app.schemas.alert import AlertCreate, AlertStatus
from app.schemas.incident import IncidentCreate, IncidentStatus, Severity as IncidentSeverity, Criticality, AffectedAsset
from app.schemas.asset import AssetCreate, AssetType, Criticality as AssetCriticality
from app.schemas.datasource import DataSourceCreate, SourceType as DSSourceType


async def seed_users(db):
    """Seed demo users."""
    user_repo = UserRepository(db)
    
    # Admin user
    admin = await user_repo.create(UserCreate(
        email="admin@cybercortex.ai",
        username="admin",
        full_name="SOC Administrator",
        password="AdminPass123!",
        role=Role.ADMIN
    ))
    print(f"Created admin user: {admin['email']}")
    
    # Analyst user
    analyst = await user_repo.create(UserCreate(
        email="analyst@cybercortex.ai",
        username="analyst",
        full_name="SOC Analyst",
        password="AnalystPass123!",
        role=Role.SOC_ANALYST
    ))
    print(f"Created analyst user: {analyst['email']}")


async def seed_assets(db):
    """Seed demo assets."""
    asset_repo = AssetRepository(db)
    
    assets = [
        AssetCreate(
            asset_id="WS-01",
            hostname="WORKSTATION-01",
            ip_addresses=["192.0.2.10"],
            asset_type=AssetType.WORKSTATION,
            operating_system="Windows 11",
            owner="user1@cybercortex.ai",
            department="Engineering",
            criticality=AssetCriticality.HIGH
        ),
        AssetCreate(
            asset_id="SRV-03",
            hostname="SERVER-03",
            ip_addresses=["192.0.2.30"],
            asset_type=AssetType.SERVER,
            operating_system="Ubuntu 22.04",
            owner="admin@cybercortex.ai",
            department="IT",
            criticality=AssetCriticality.CRITICAL
        ),
        AssetCreate(
            asset_id="SRV-05",
            hostname="SERVER-05",
            ip_addresses=["192.0.2.35"],
            asset_type=AssetType.SERVER,
            operating_system="Ubuntu 22.04",
            owner="admin@cybercortex.ai",
            department="IT",
            criticality=AssetCriticality.HIGH
        ),
        AssetCreate(
            asset_id="AUTH-01",
            hostname="AUTH-SERVER-01",
            ip_addresses=["192.0.2.50"],
            asset_type=AssetType.SERVER,
            operating_system="Windows Server 2022",
            owner="admin@cybercortex.ai",
            department="IT",
            criticality=AssetCriticality.CRITICAL
        ),
        AssetCreate(
            asset_id="DB-ADMIN",
            hostname="DB-ADMIN-01",
            ip_addresses=["192.0.2.100"],
            asset_type=AssetType.DATABASE,
            operating_system="Ubuntu 22.04",
            owner="admin@cybercortex.ai",
            department="IT",
            criticality=AssetCriticality.CRITICAL
        ),
    ]
    
    for asset_data in assets:
        asset = await asset_repo.create(asset_data)
        print(f"Created asset: {asset['asset_id']}")


async def seed_data_sources(db):
    """Seed demo data sources."""
    ds_repo = DataSourceRepository(db)
    
    sources = [
        DataSourceCreate(
            source_id="windows-security",
            name="Windows Security",
            type=DSSourceType.WINDOWS,
            description="Windows Event Logs",
            enabled=True
        ),
        DataSourceCreate(
            source_id="firewall-01",
            name="Corporate Firewall",
            type=DSSourceType.FIREWALL,
            description="Network firewall logs",
            enabled=True
        ),
        DataSourceCreate(
            source_id="proxy-01",
            name="Web Proxy",
            type=DSSourceType.PROXY,
            description="Web proxy logs",
            enabled=True
        ),
        DataSourceCreate(
            source_id="edr-01",
            name="Endpoint Detection",
            type=DSSourceType.EDR,
            description="EDR agent logs",
            enabled=True
        ),
    ]
    
    for ds_data in sources:
        ds = await ds_repo.create(ds_data)
        print(f"Created data source: {ds['source_id']}")


async def seed_events(db):
    """Seed demo security events."""
    event_repo = EventRepository(db)
    
    base_time = datetime.utcnow()
    
    events = []
    for i in range(50):
        event = SecurityEventCreate(
            event_id=f"EVT-{1000 + i}",
            source="windows-security",
            source_type=SourceType.WINDOWS,
            raw_event={"original_message": f"Event {i}"},
            normalized_event=NormalizedEvent(
                timestamp=base_time - timedelta(minutes=i*5),
                event_type="Authentication",
                category="Security",
                severity=Severity.LOW if i % 3 != 0 else (Severity.HIGH if i % 3 == 1 else Severity.CRITICAL),
                source_ip="192.0.2.200" if i % 2 == 0 else "198.51.100.50",
                destination_ip="192.0.2.10",
                source_port=50000 + i,
                destination_port=3389,
                protocol="TCP",
                user=f"user{i % 5}@cybercortex.ai",
                host="WORKSTATION-01",
                description=f"Authentication event {i}"
            )
        )
        events.append(event)
    
    # Create in bulk
    created = await event_repo.create_bulk(events)
    print(f"Created {len(created)} security events")


async def seed_alerts(db):
    """Seed demo alerts."""
    alert_repo = AlertRepository(db)
    
    alerts = [
        AlertCreate(
            alert_id="ALT-2026-0001",
            title="Brute Force Attack Detected",
            description="Multiple failed authentication attempts from external IP",
            severity=Severity.CRITICAL,
            source="windows-security",
            rule_id="RULE-001",
            confidence_score=92,
            mitre_techniques=["T1110"],
            iocs=[{"type": "IP", "value": "198.51.100.50", "confidence": 0.92}]
        ),
        AlertCreate(
            alert_id="ALT-2026-0002",
            title="Suspicious PowerShell Execution",
            description="PowerShell execution with encoded command detected",
            severity=Severity.HIGH,
            source="edr-01",
            rule_id="RULE-002",
            confidence_score=85,
            mitre_techniques=["T1059"]
        ),
        AlertCreate(
            alert_id="ALT-2026-0003",
            title="Unusual Login Activity",
            description="Login from unusual geographic location",
            severity=Severity.HIGH,
            source="windows-security",
            rule_id="RULE-003",
            confidence_score=78,
            mitre_techniques=["T1078"]
        ),
    ]
    
    for alert_data in alerts:
        alert = await alert_repo.create(alert_data)
        print(f"Created alert: {alert['alert_id']}")


async def seed_incidents(db):
    """Seed demo incidents."""
    incident_repo = IncidentRepository(db)
    
    incidents = [
        IncidentCreate(
            incident_id="CC-2026-1042",
            title="Possible Lateral Movement",
            description="Detection of suspicious lateral movement patterns from workstation WS-01 to multiple internal servers",
            severity=IncidentSeverity.CRITICAL,
            affected_assets=[
                AffectedAsset(type="DEVICE", id="WS-01", name="WORKSTATION-01", criticality=Criticality.HIGH),
                AffectedAsset(type="HOST", id="SRV-03", name="SERVER-03", criticality=Criticality.CRITICAL),
                AffectedAsset(type="HOST", id="SRV-05", name="SERVER-05", criticality=Criticality.HIGH),
            ],
            mitre_techniques=["T1021", "T1078"],
            indicators=[{"type": "IP", "value": "192.0.2.200", "confidence": 0.92}],
            recommended_actions=[
                "Isolate affected workstation WS-01",
                "Investigate credential usage on affected servers",
                "Reset credentials for affected accounts",
                "Review network logs for additional lateral movement",
                "Enable enhanced monitoring on critical servers"
            ]
        ),
        IncidentCreate(
            incident_id="CC-2026-1041",
            title="Suspicious PowerShell Execution",
            description="Suspicious PowerShell execution detected on SRV-03",
            severity=IncidentSeverity.HIGH,
            affected_assets=[
                AffectedAsset(type="HOST", id="SRV-03", name="SERVER-03", criticality=Criticality.CRITICAL),
            ],
            mitre_techniques=["T1059"],
            recommended_actions=[
                "Investigate PowerShell command execution",
                "Check for process injection",
                "Review user activity on SRV-03"
            ]
        ),
        IncidentCreate(
            incident_id="CC-2026-1040",
            title="Brute Force Attack Detected",
            description="Brute force attack detected against AUTH-01",
            severity=IncidentSeverity.CRITICAL,
            affected_assets=[
                AffectedAsset(type="HOST", id="AUTH-01", name="AUTH-SERVER-01", criticality=Criticality.CRITICAL),
            ],
            mitre_techniques=["T1110"],
            recommended_actions=[
                "Block source IP addresses",
                "Investigate credential compromise",
                "Review authentication logs"
            ]
        ),
        IncidentCreate(
            incident_id="CC-2026-1039",
            title="Unusual Login Activity",
            description="Unusual login activity detected for user account",
            severity=IncidentSeverity.HIGH,
            affected_assets=[
                AffectedAsset(type="USER", id="USER-892", name="user1@cybercortex.ai", criticality=Criticality.MEDIUM),
            ],
            mitre_techniques=["T1078"],
            recommended_actions=[
                "Verify user identity",
                "Check for credential reuse",
                "Review login location"
            ]
        ),
        IncidentCreate(
            incident_id="CC-2026-1038",
            title="Port Scan Detected",
            description="Port scan activity detected from external source",
            severity=IncidentSeverity.MEDIUM,
            affected_assets=[
                AffectedAsset(type="NETWORK_DEVICE", id="FW-EXT-01", name="Corporate Firewall", criticality=Criticality.HIGH),
            ],
            mitre_techniques=["T1046"],
            recommended_actions=[
                "Analyze scan pattern",
                "Block scanning IP if malicious",
                "Review firewall rules"
            ]
        ),
        IncidentCreate(
            incident_id="CC-2026-1037",
            title="Credential Compromise",
            description="Potential credential compromise detected for database admin account",
            severity=IncidentSeverity.CRITICAL,
            affected_assets=[
                AffectedAsset(type="DATABASE", id="DB-ADMIN", name="DB-ADMIN-01", criticality=Criticality.CRITICAL),
            ],
            mitre_techniques=["T1110", "T1078"],
            recommended_actions=[
                "Immediate credential reset",
                "Rotate database credentials",
                "Investigate database access logs",
                "Enable database activity monitoring"
            ]
        ),
    ]
    
    for incident_data in incidents:
        incident = await incident_repo.create(incident_data)
        print(f"Created incident: {incident['incident_id']}")


async def main():
    """Main seed function."""
    print("Starting data seed...")
    
    # Connect to MongoDB
    await MongoDB.connect()
    db = await get_database()
    
    # Seed data
    await seed_users(db)
    await seed_assets(db)
    await seed_data_sources(db)
    await seed_events(db)
    await seed_alerts(db)
    await seed_incidents(db)
    
    # Close connection
    await MongoDB.close()
    
    print("Data seed completed successfully!")


if __name__ == "__main__":
    asyncio.run(main())
