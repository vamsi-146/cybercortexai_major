"""Alert generation service for creating alerts from detection results."""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.database.mongodb import get_database


class AlertGenerationService:
    """Service for generating alerts from detection results."""

    @staticmethod
    async def generate_alert(
        detection_result: Dict[str, Any],
        event: Dict[str, Any],
        correlation_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Generate an alert from a detection result.

        Args:
            detection_result: The detection result from a rule
            event: The triggering event
            correlation_context: Correlation context

        Returns:
            Generated alert dict
        """
        db = await get_database()
        alerts_collection = db.alerts

        # Check for existing similar alert (deduplication)
        existing_alert = await AlertGenerationService._find_existing_alert(
            alerts_collection,
            detection_result,
            event
        )

        if existing_alert:
            # Update existing alert instead of creating new one
            return await AlertGenerationService._update_existing_alert(
                alerts_collection,
                existing_alert,
                detection_result,
                event,
                correlation_context
            )
        else:
            # Create new alert
            return await AlertGenerationService._create_new_alert(
                alerts_collection,
                detection_result,
                event,
                correlation_context
            )

    @staticmethod
    async def _find_existing_alert(
        alerts_collection,
        detection_result: Dict[str, Any],
        event: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Find an existing similar alert for deduplication.

        Args:
            alerts_collection: MongoDB alerts collection
            detection_result: Detection result
            event: Triggering event

        Returns:
            Existing alert or None
        """
        rule_id = detection_result.get("rule_id")
        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - detection_result.get("time_window_seconds", 300)

        # Look for alerts from same rule within correlation window
        query = {
            "rule_id": rule_id,
            "status": {"$in": ["open", "in_progress"]},
            "last_seen": {"$gte": window_start}
        }

        # Add entity-based matching if available
        if event.get("username"):
            query["affected_users"] = event["username"]
        elif event.get("src_ip"):
            query["affected_ips"] = event["src_ip"]

        return await alerts_collection.find_one(query)

    @staticmethod
    async def _create_new_alert(
        alerts_collection,
        detection_result: Dict[str, Any],
        event: Dict[str, Any],
        correlation_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create a new alert."""
        alert_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()

        alert = {
            "alert_id": alert_id,
            "rule_id": detection_result.get("rule_id"),
            "rule_name": detection_result.get("rule_name"),
            "title": f"{detection_result.get('rule_name')}: {detection_result.get('reason', 'Detection')}",
            "description": detection_result.get("description", ""),
            "severity": detection_result.get("severity", "medium"),
            "status": "open",
            "source": "rule_engine",
            "event_ids": [event.get("event_id")],
            "affected_assets": [event.get("hostname"), event.get("device_id")] if event.get("hostname") or event.get("device_id") else [],
            "affected_users": [event.get("username")] if event.get("username") else [],
            "affected_ips": [event.get("src_ip")] if event.get("src_ip") else [],
            "mitre_techniques": detection_result.get("mitre_techniques", []),
            "risk_score": AlertGenerationService._calculate_risk_score(detection_result, event),
            "first_seen": timestamp,
            "last_seen": timestamp,
            "occurrence_count": 1,
            "detection_evidence": {
                "triggering_event_id": event.get("event_id"),
                "triggering_event_timestamp": event.get("timestamp"),
                "reason": detection_result.get("reason"),
                "evidence": detection_result.get("evidence", []),
                "correlated_event_ids": correlation_context.get("correlated_event_ids", []),
                "threshold_used": detection_result.get("threshold"),
                "time_window_seconds": detection_result.get("time_window_seconds"),
            },
            "correlation_data": correlation_context,
            "created_at": timestamp,
            "updated_at": timestamp,
        }

        await alerts_collection.insert_one(alert)
        return alert

    @staticmethod
    async def _update_existing_alert(
        alerts_collection,
        existing_alert: Dict[str, Any],
        detection_result: Dict[str, Any],
        event: Dict[str, Any],
        correlation_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing alert with new occurrence."""
        alert_id = existing_alert["alert_id"]
        timestamp = datetime.utcnow()

        # Update the alert
        update = {
            "$set": {
                "last_seen": timestamp,
                "updated_at": timestamp,
            },
            "$inc": {
                "occurrence_count": 1,
            },
            "$addToSet": {
                "event_ids": event.get("event_id"),
            }
        }

        # Update affected entities if new
        if event.get("username") and event["username"] not in existing_alert.get("affected_users", []):
            update["$addToSet"]["affected_users"] = event["username"]
        if event.get("src_ip") and event["src_ip"] not in existing_alert.get("affected_ips", []):
            update["$addToSet"]["affected_ips"] = event["src_ip"]

        await alerts_collection.update_one({"alert_id": alert_id}, update)

        # Return updated alert
        updated = await alerts_collection.find_one({"alert_id": alert_id})
        return updated

    @staticmethod
    def _calculate_risk_score(detection_result: Dict[str, Any], event: Dict[str, Any]) -> int:
        """
        Calculate a deterministic risk score (0-100).

        Args:
            detection_result: Detection result
            event: Triggering event

        Returns:
            Risk score 0-100
        """
        score = 50  # Base score

        # Severity weight
        severity = detection_result.get("severity", "medium")
        severity_weights = {
            "critical": 30,
            "high": 20,
            "medium": 10,
            "low": 0,
        }
        score += severity_weights.get(severity, 10)

        # MITRE technique count
        mitre_count = len(detection_result.get("mitre_techniques", []))
        score += min(mitre_count * 5, 15)

        # Correlation score bonus
        correlation_score = correlation_context.get("correlation_score", 0)
        score += min(correlation_score * 0.1, 20)

        # Privileged account bonus
        if event.get("category") == "privilege":
            score += 15

        # External IP bonus
        if event.get("src_ip"):
            from app.enrichment.service import EnrichmentService
            ip_type = EnrichmentService.classify_ip(event["src_ip"])
            if ip_type == "public":
                score += 10

        return min(score, 100)
