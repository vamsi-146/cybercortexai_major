"""Brute Force Detection Rule."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database
from .base import BaseDetectionRule


class BruteForceRule(BaseDetectionRule):
    """
    Detect brute force authentication attacks.

    Triggers when multiple failed authentication attempts occur
    from the same source IP or against the same username
    within a configured time window.
    """

    def __init__(self):
        super().__init__()
        self.name = "Brute Force Detection"
        self.description = "Detects repeated failed authentication attempts indicating brute force attacks"
        self.enabled = True
        self.severity = "high"
        self.source_types = ["windows", "linux"]
        self.event_types = ["authentication"]
        self.mitre_techniques = ["T1110"]  # Brute Force
        self.threshold = 5  # Number of failures
        self.time_window_seconds = 300  # 5 minutes

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this event is part of a brute force attack."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Only check failed authentication events
        if event.get("action") not in ["login_failure", "account_locked", "invalid_user"]:
            return None

        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=self.time_window_seconds)

        # Count failures by source IP
        if event.get("src_ip"):
            ip_failures = await events_collection.count_documents({
                "src_ip": event["src_ip"],
                "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                "timestamp": {"$gte": window_start, "$lte": timestamp}
            })

            if ip_failures >= self.threshold:
                # Get the specific events for evidence
                failure_events = await events_collection.find({
                    "src_ip": event["src_ip"],
                    "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                    "timestamp": {"$gte": window_start, "$lte": timestamp}
                }).to_list(length=50)

                evidence = [
                    f"Detected {ip_failures} failed authentication attempts from {event['src_ip']}",
                    f"Threshold: {self.threshold} failures within {self.time_window_seconds} seconds",
                    f"Targeted users: {list(set(e.get('username') for e in failure_events if e.get('username')))}"
                ]

                return self.create_detection_result(
                    event,
                    context,
                    f"Brute force detected from IP {event['src_ip']} with {ip_failures} failures",
                    evidence
                )

        # Count failures by username
        if event.get("username"):
            user_failures = await events_collection.count_documents({
                "username": event["username"],
                "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                "timestamp": {"$gte": window_start, "$lte": timestamp}
            })

            if user_failures >= self.threshold:
                failure_events = await events_collection.find({
                    "username": event["username"],
                    "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                    "timestamp": {"$gte": window_start, "$lte": timestamp}
                }).to_list(length=50)

                source_ips = list(set(e.get('src_ip') for e in failure_events if e.get('src_ip')))

                evidence = [
                    f"Detected {user_failures} failed authentication attempts for user {event['username']}",
                    f"Threshold: {self.threshold} failures within {self.time_window_seconds} seconds",
                    f"Source IPs: {source_ips}"
                ]

                return self.create_detection_result(
                    event,
                    context,
                    f"Brute force detected against user {event['username']} with {user_failures} failures",
                    evidence
                )

        return None
