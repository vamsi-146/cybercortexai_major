"""Port Scan Detection Rule."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database
from .base import BaseDetectionRule


class PortScanRule(BaseDetectionRule):
    """
    Detect port scanning activity.

    Triggers when one source IP attempts connections to many
    different destination ports on the same host within a time window.
    """

    def __init__(self):
        super().__init__()
        self.name = "Port Scan Detection"
        self.description = "Detects port scanning activity from a single source IP"
        self.enabled = True
        self.severity = "medium"
        self.source_types = ["firewall"]
        self.event_types = ["network_connection"]
        self.mitre_techniques = ["T1046", "T1018"]  # Network Service Scanning, Remote System Discovery
        self.threshold = 15  # Number of unique ports
        self.time_window_seconds = 60  # 1 minute

    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Evaluate if this event is part of a port scan."""
        if not self.check_source_type(event) or not self.check_event_type(event):
            return None

        # Need source IP and destination IP
        if not event.get("src_ip") or not event.get("dst_ip"):
            return None

        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=self.time_window_seconds)

        # Get all connections from this source to this destination in the window
        connections = await events_collection.find({
            "src_ip": event["src_ip"],
            "dst_ip": event["dst_ip"],
            "timestamp": {"$gte": window_start, "$lte": timestamp}
        }).to_list(length=200)

        # Count unique destination ports
        unique_ports = set()
        for conn in connections:
            if conn.get("dst_port"):
                unique_ports.add(conn["dst_port"])

        if len(unique_ports) >= self.threshold:
            evidence = [
                f"Detected {len(unique_ports)} unique destination ports from {event['src_ip']} to {event['dst_ip']}",
                f"Threshold: {self.threshold} ports within {self.time_window_seconds} seconds",
                f"Scanned ports: {sorted(list(unique_ports))[:20]}"  # Show first 20
            ]

            if len(unique_ports) > 20:
                evidence.append(f"... and {len(unique_ports) - 20} more ports")

            return self.create_detection_result(
                event,
                context,
                f"Port scan detected from {event['src_ip']} to {event['dst_ip']} with {len(unique_ports)} ports",
                evidence
            )

        return None
