"""Account Lockout Burst Detection Rule."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database
from .base import BaseDetectionRule


class AccountLockoutBurstRule(BaseDetectionRule):
    """
    Detect unusual patterns of account lockouts.

    Triggers when:
    1. Multiple accounts are locked out in a short time window (burst)
    2. A single account is locked out repeatedly
    This may indicate brute force attacks or credential spraying.
    """

    def __init__(self):
        super().__init__()
        self.name = "Account Lockout Burst Detection"
        self.description = "Detects unusual patterns of account lockouts"
        self.enabled = True
        self.severity = "high"
        self.source_types = ["windows", "linux"]
        self.event_types = ["authentication"]
        self.mitre_techniques = ["T1110"]  # Brute Force
        self.threshold = 3  # Number of lockouts
        self.time_window_seconds = 300  # 5 minutes

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this event is part of an account lockout burst."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Check for account lockout event
        if event.get("action") != "account_locked":
            return None

        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=self.time_window_seconds)

        # Option 1: Check for multiple different accounts locked out (credential spraying)
        if event.get("src_ip"):
            lockouts = await events_collection.find({
                "action": "account_locked",
                "src_ip": event["src_ip"],
                "timestamp": {"$gte": window_start, "$lte": timestamp}
            }).to_list(length=50)

            unique_users = set(e.get("username") for e in lockouts if e.get("username"))

            if len(unique_users) >= self.threshold:
                evidence = [
                    f"Detected {len(unique_users)} different accounts locked out from {event['src_ip']}",
                    f"Threshold: {self.threshold} accounts within {self.time_window_seconds} seconds",
                    f"Locked accounts: {list(unique_users)}",
                    f"Total lockout events: {len(lockouts)}"
                ]

                return self.create_detection_result(
                    event,
                    context,
                    f"Account lockout burst from {event['src_ip']} affecting {len(unique_users)} accounts",
                    evidence
                )

        # Option 2: Check for repeated lockouts of the same account
        if event.get("username"):
            user_lockouts = await events_collection.find({
                "action": "account_locked",
                "username": event["username"],
                "timestamp": {"$gte": window_start, "$lte": timestamp}
            }).to_list(length=50)

            if len(user_lockouts) >= self.threshold:
                source_ips = list(set(e.get('src_ip') for e in user_lockouts if e.get('src_ip')))

                evidence = [
                    f"User {event['username']} locked out {len(user_lockouts)} times",
                    f"Threshold: {self.threshold} lockouts within {self.time_window_seconds} seconds",
                    f"Source IPs: {source_ips}",
                    f"Hostnames: {list(set(e.get('hostname') for e in user_lockouts if e.get('hostname')))}"
                ]

                return self.create_detection_result(
                    event,
                    context,
                    f"Repeated account lockouts for {event['username']}: {len(user_lockouts)} times",
                    evidence
                )

        return None
