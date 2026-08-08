"""Success After Multiple Failures Detection Rule."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database
from .base import BaseDetectionRule


class SuccessAfterFailuresRule(BaseDetectionRule):
    """
    Detect successful authentication following multiple failures.

    This may indicate credential compromise or successful password guessing.
    """

    def __init__(self):
        super().__init__()
        self.name = "Success After Failures Detection"
        self.description = "Detects successful logins following repeated authentication failures"
        self.enabled = True
        self.severity = "high"
        self.source_types = ["windows", "linux"]
        self.event_types = ["authentication"]
        self.mitre_techniques = ["T1078", "T1110"]  # Valid Accounts, Brute Force
        self.threshold = 3  # Minimum failures before success
        self.time_window_seconds = 300  # 5 minutes

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this successful login follows multiple failures."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Only check successful authentication events
        if event.get("action") != "login_success":
            return None

        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=self.time_window_seconds)

        # Check for failures by same username
        if event.get("username"):
            user_failures = await events_collection.count_documents({
                "username": event["username"],
                "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                "timestamp": {"$gte": window_start, "$lt": timestamp}
            })

            if user_failures >= self.threshold:
                failure_events = await events_collection.find({
                    "username": event["username"],
                    "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                    "timestamp": {"$gte": window_start, "$lt": timestamp}
                }).to_list(length=50)

                source_ips = list(set(e.get('src_ip') for e in failure_events if e.get('src_ip')))

                evidence = [
                    f"User {event['username']} had {user_failures} failed authentication attempts",
                    f"Threshold: {self.threshold} failures within {self.time_window_seconds} seconds",
                    f"Successful login from {event.get('src_ip', 'unknown IP')}",
                    f"Failure source IPs: {source_ips}"
                ]

                return self.create_detection_result(
                    event,
                    context,
                    f"Successful login for {event['username']} after {user_failures} failures",
                    evidence
                )

        # Check for failures from same source IP
        if event.get("src_ip"):
            ip_failures = await events_collection.count_documents({
                "src_ip": event["src_ip"],
                "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                "timestamp": {"$gte": window_start, "$lt": timestamp}
            })

            if ip_failures >= self.threshold:
                failure_events = await events_collection.find({
                    "src_ip": event["src_ip"],
                    "action": {"$in": ["login_failure", "account_locked", "invalid_user"]},
                    "timestamp": {"$gte": window_start, "$lt": timestamp}
                }).to_list(length=50)

                usernames = list(set(e.get('username') for e in failure_events if e.get('username')))

                evidence = [
                    f"Source IP {event['src_ip']} had {ip_failures} failed authentication attempts",
                    f"Threshold: {self.threshold} failures within {self.time_window_seconds} seconds",
                    f"Successful login for {event.get('username', 'unknown user')}",
                    f"Targeted usernames: {usernames}"
                ]

                return self.create_detection_result(
                    event,
                    context,
                    f"Successful login from {event['src_ip']} after {ip_failures} failures",
                    evidence
                )

        return None
