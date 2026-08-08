"""New Account + Privilege Escalation Detection Rule."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database
from .base import BaseDetectionRule


class NewAccountPrivilegeEscalationRule(BaseDetectionRule):
    """
    Detect new user account creation followed by privilege escalation.

    This is a multi-event correlation rule that triggers when:
    1. A new user account is created
    2. Followed by addition to a privileged group
    Within a configured time window.
    """

    def __init__(self):
        super().__init__()
        self.name = "New Account + Privilege Escalation Detection"
        self.description = "Detects new account creation followed by privilege escalation"
        self.enabled = True
        self.severity = "critical"
        self.source_types = ["windows", "linux"]
        self.event_types = ["account"]
        self.mitre_techniques = ["T1136", "T1098"]  # Create Account, Account Manipulation
        self.threshold = 1  # One correlation needed
        self.time_window_seconds = 900  # 15 minutes

        # Privileged group names
        self.privileged_groups = [
            "Administrators",
            "Domain Admins",
            "Enterprise Admins",
            "root",
            "wheel",
            "sudo",
        ]

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this event completes a new account + privilege escalation pattern."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Check for group modification event
        if event.get("action") != "group_member_added":
            return None

        username = event.get("username")
        if not username:
            return None

        group_name = event.get("group_name", "").lower()
        is_privileged = any(
            privileged.lower() in group_name
            for privileged in self.privileged_groups
        )

        if not is_privileged:
            return None

        # Look for recent account creation for this user
        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=self.time_window_seconds)

        account_creation = await events_collection.find_one({
            "username": username,
            "action": "account_created",
            "timestamp": {"$gte": window_start, "$lt": timestamp}
        })

        if account_creation:
            evidence = [
                f"User {username} was created at {account_creation.get('timestamp')}",
                f"Within {self.time_window_seconds} seconds, user was added to privileged group: {group_name}",
                f"Account creation event ID: {account_creation.get('event_id')}",
                f"Privilege escalation event ID: {event.get('event_id')}"
            ]

            return self.create_detection_result(
                event,
                context,
                f"New account {username} created and immediately escalated to privileged group {group_name}",
                evidence
            )

        return None
