"""Incident grouping service for grouping related alerts into incidents."""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database


class IncidentGroupingService:
    """Service for grouping related alerts into incidents."""

    @staticmethod
    async def group_alert_into_incident(alert: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Group an alert into an existing incident or create a new one.

        Args:
            alert: The alert to group

        Returns:
            The incident (existing or newly created)
        """
        db = await get_database()
        incidents_collection = db.incidents

        # Try to find existing incident
        existing_incident = await IncidentGroupingService._find_existing_incident(
            incidents_collection,
            alert
        )

        if existing_incident:
            # Add alert to existing incident
            return await IncidentGroupingService._add_alert_to_incident(
                incidents_collection,
                existing_incident,
                alert
            )
        else:
            # Create new incident
            return await IncidentGroupingService._create_new_incident(
                incidents_collection,
                alert
            )

    @staticmethod
    async def _find_existing_incident(
        incidents_collection,
        alert: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Find an existing incident that this alert should belong to.

        Args:
            incidents_collection: MongoDB incidents collection
            alert: The alert

        Returns:
            Existing incident or None
        """
        timestamp = datetime.utcnow()
        window_start = timestamp - timedelta(hours=24)  # 24-hour window

        # Build query based on alert entities
        query = {
            "status": {"$in": ["open", "in_progress"]},
            "created_at": {"$gte": window_start}
        }

        # Match by affected user
        if alert.get("affected_users"):
            query["affected_users"] = {"$in": alert["affected_users"]}

        # Match by affected IP
        elif alert.get("affected_ips"):
            query["affected_ips"] = {"$in": alert["affected_ips"]}

        # Match by affected asset
        elif alert.get("affected_assets"):
            query["affected_assets"] = {"$in": alert["affected_assets"]}

        # Match by MITRE technique overlap
        elif alert.get("mitre_techniques"):
            query["mitre_techniques"] = {"$in": alert["mitre_techniques"]}

        # Find most recent matching incident
        return await incidents_collection.find_one(query, sort=[("created_at", -1)])

    @staticmethod
    async def _add_alert_to_incident(
        incidents_collection,
        incident: Dict[str, Any],
        alert: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add an alert to an existing incident."""
        incident_id = incident["incident_id"]
        timestamp = datetime.utcnow()

        update = {
            "$set": {
                "updated_at": timestamp,
            },
            "$inc": {
                "alert_count": 1,
            },
            "$addToSet": {
                "alert_ids": alert["alert_id"],
            }
        }

        # Update affected entities
        if alert.get("affected_users"):
            update["$addToSet"]["affected_users"] = {"$each": alert["affected_users"]}
        if alert.get("affected_ips"):
            update["$addToSet"]["affected_ips"] = {"$each": alert["affected_ips"]}
        if alert.get("affected_assets"):
            update["$addToSet"]["affected_assets"] = {"$each": alert["affected_assets"]}

        # Update MITRE techniques
        if alert.get("mitre_techniques"):
            update["$addToSet"]["mitre_techniques"] = {"$each": alert["mitre_techniques"]}

        # Recalculate risk score
        updated_risk = IncidentGroupingService._calculate_incident_risk(incident, alert)
        update["$set"]["risk_score"] = updated_risk

        await incidents_collection.update_one({"incident_id": incident_id}, update)

        # Return updated incident
        updated = await incidents_collection.find_one({"incident_id": incident_id})
        return updated

    @staticmethod
    async def _create_new_incident(
        incidents_collection,
        alert: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new incident from an alert."""
        incident_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        incident = {
            "incident_id": incident_id,
            "title": IncidentGroupingService._generate_incident_title(alert),
            "description": IncidentGroupingService._generate_incident_description(alert),
            "severity": alert.get("severity", "medium"),
            "status": "open",
            "alert_ids": [alert["alert_id"]],
            "alert_count": 1,
            "event_ids": alert.get("event_ids", []),
            "affected_assets": alert.get("affected_assets", []),
            "affected_users": alert.get("affected_users", []),
            "affected_ips": alert.get("affected_ips", []),
            "mitre_techniques": alert.get("mitre_techniques", []),
            "risk_score": alert.get("risk_score", 50),
            "timeline": IncidentGroupingService._create_initial_timeline(alert),
            "indicators": IncidentGroupingService._extract_indicators(alert),
            "recommendations": IncidentGroupingService._generate_recommendations(alert),
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        await incidents_collection.insert_one(incident)
        return incident

    @staticmethod
    def _generate_incident_title(alert: Dict[str, Any]) -> str:
        """Generate a title for the incident."""
        rule_name = alert.get("rule_name", "Security Incident")
        entity = alert.get("affected_users", alert.get("affected_ips", ["Unknown"]))[0]
        return f"{rule_name} - {entity}"

    @staticmethod
    def _generate_incident_description(alert: Dict[str, Any]) -> str:
        """Generate a description for the incident."""
        rule_name = alert.get("rule_name", "Security Incident")
        reason = alert.get("detection_evidence", {}).get("reason", "Unknown reason")
        return f"{rule_name}: {reason}"

    @staticmethod
    def _calculate_incident_risk(incident: Dict[str, Any], alert: Dict[str, Any]) -> int:
        """Calculate updated incident risk score."""
        # Average of existing and new alert risk, weighted by alert count
        existing_risk = incident.get("risk_score", 50)
        new_risk = alert.get("risk_score", 50)
        alert_count = incident.get("alert_count", 1)

        # Simple average
        return int((existing_risk * alert_count + new_risk) / (alert_count + 1))

    @staticmethod
    def _create_initial_timeline(alert: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Create initial timeline from alert."""
        return [
            {
                "event": f"Alert triggered: {alert.get('rule_name')}",
                "timestamp": alert.get("first_seen"),
                "severity": alert.get("severity"),
                "description": alert.get("detection_evidence", {}).get("reason", ""),
            }
        ]

    @staticmethod
    def _extract_indicators(alert: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract indicators from alert."""
        indicators = []

        # IP indicators
        for ip in alert.get("affected_ips", []):
            indicators.append({
                "type": "ip",
                "value": ip,
                "confidence": 0.8,
            })

        # User indicators
        for user in alert.get("affected_users", []):
            indicators.append({
                "type": "user",
                "value": user,
                "confidence": 0.7,
            })

        return indicators

    @staticmethod
    def _generate_recommendations(alert: Dict[str, Any]) -> List[str]:
        """Generate initial recommendations based on alert."""
        recommendations = []

        severity = alert.get("severity", "medium")
        if severity in ["high", "critical"]:
            recommendations.append("Immediately investigate the affected user/host")
            recommendations.append("Review recent authentication logs for the affected entity")

        if alert.get("affected_users"):
            recommendations.append("Consider temporarily locking the affected user account")

        if alert.get("affected_ips"):
            recommendations.append("Block the source IP if external")

        recommendations.append("Document findings in incident notes")

        return recommendations
