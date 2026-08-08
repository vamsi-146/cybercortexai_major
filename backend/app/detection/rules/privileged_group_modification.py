"""Privileged Group Modification Detection Rule."""

from typing import Dict, Any, List, Optional
from .base import BaseDetectionRule


class PrivilegedGroupModificationRule(BaseDetectionRule):
    """
    Detect modifications to privileged security groups.

    Triggers when a user is added to sensitive groups like
    Administrators, Domain Admins, or similar privileged groups.
    """

    def __init__(self):
        super().__init__()
        self.name = "Privileged Group Modification Detection"
        self.description = "Detects additions of users to privileged security groups"
        self.enabled = True
        self.severity = "high"
        self.source_types = ["windows", "linux"]
        self.event_types = ["account"]
        self.mitre_techniques = ["T1098"]  # Account Manipulation
        self.threshold = 1  # Any privileged group modification
        self.time_window_seconds = 0  # Not time-based

        # Privileged group names
        self.privileged_groups = [
            "Administrators",
            "Domain Admins",
            "Enterprise Admins",
            "Schema Admins",
            "Backup Operators",
            "Account Operators",
            "root",
            "wheel",
            "sudo",
            "adm",
        ]

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this event is a privileged group modification."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Check for group modification actions
        action = event.get("action", "")
        if action not in ["group_member_added", "account_created"]:
            return None

        group_name = event.get("group_name", "").lower()
        username = event.get("username", "")
        hostname = event.get("hostname", "")

        # Check if it's a privileged group
        is_privileged = any(
            privileged.lower() in group_name
            for privileged in self.privileged_groups
        )

        if is_privileged:
            evidence = [
                f"User {username} added to privileged group: {group_name}",
                f"Group modification detected on {hostname}",
                f"Privileged group matches: {group_name}"
            ]

            return self.create_detection_result(
                event,
                context,
                f"Privileged group modification: {username} added to {group_name}",
                evidence
            )

        return None
