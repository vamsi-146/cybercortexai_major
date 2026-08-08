"""Multiple Host Scan Detection Rule."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database
from .base import BaseDetectionRule


class MultipleHostScanRule(BaseDetectionRule):
    """
    Detect scanning of multiple internal hosts.

    Triggers when one source IP contacts many different
    destination hosts within a short time window.
    """

    def __init__(self):
        super().__init__()
        self.name = "Multiple Host Scan Detection"
        self.description = "Detects scanning activity across multiple destination hosts"
        self.enabled = True
        self.severity = "medium"
        self.source_types = ["firewall"]
        self.event_types = ["network_connection"]
        self.mitre_techniques = ["T1018"]  # Remote System Discovery
        self.threshold = 10  # Number of unique hosts
        self.time_window_seconds = 300  # 5 minutes

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this event is part of a multi-host scan."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Need source IP
        if not event.get("src_ip"):
            return None

        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=self.time_window_seconds)

        # Get all connections from this source IP in the window
        connections = await events_collection.find({
            "src_ip": event["src_ip"],
            "timestamp": {"$gte": window_start, "$lte": timestamp}
        }).to_list(length=500)

        # Count unique destination IPs
        unique_dst_ips = set()
        for conn in connections:
            if conn.get("dst_ip"):
                unique_dst_ips.add(conn["dst_ip"])

        if len(unique_dst_ips) >= self.threshold:
            evidence = [
                f"Detected {len(unique_dst_ips)} unique destination hosts from {event['src_ip']}",
                f"Threshold: {self.threshold} hosts within {self.time_window_seconds} seconds",
                f"Scanned hosts: {sorted(list(unique_dst_ips))[:15]}"  # Show first 15
            ]

            if len(unique_dst_ips) > 15:
                evidence.append(f"... and {len(unique_dst_ips) - 15} more hosts")

            return self.create_detection_result(
                event,
                context,
                f"Multi-host scan detected from {event['src_ip']} with {len(unique_dst_ips)} hosts",
                evidence
            )

        return None
