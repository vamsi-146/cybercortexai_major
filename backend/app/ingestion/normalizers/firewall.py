"""Firewall event normalizer."""

import uuid
from typing import Dict, Any
from datetime import datetime
from .base import BaseNormalizer


class FirewallNormalizer(BaseNormalizer):
    """Normalizer for firewall and network security logs."""

    def normalize(self, parsed_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize firewall event to CyberCortex common model."""
        normalized = {
            "event_id": str(uuid.uuid4()),
            "timestamp": parsed_event.get("timestamp", datetime.utcnow()),
            "received_at": datetime.utcnow(),
            "source_type": "firewall",
            "source_name": parsed_event.get("source_name", "Firewall Log"),
            "source_product": "Network Firewall",
            "event_type": "network_connection",
            "category": "network",
            "severity": parsed_event.get("severity", "low"),
            "message": self._generate_message(parsed_event),
            "src_ip": parsed_event.get("src_ip"),
            "src_port": parsed_event.get("src_port"),
            "dst_ip": parsed_event.get("dst_ip"),
            "dst_port": parsed_event.get("dst_port"),
            "protocol": parsed_event.get("protocol"),
            "username": None,
            "hostname": None,
            "device_id": None,
            "process_name": None,
            "process_id": None,
            "parent_process_name": None,
            "command_line": None,
            "file_path": None,
            "file_hash": None,
            "action": parsed_event.get("action"),
            "outcome": parsed_event.get("action"),
            "event_code": parsed_event.get("event_code"),
            "authentication_type": None,
            "resource": None,
            "raw_event": parsed_event.get("raw_event"),
            "metadata": {},
            "tags": [],
            "mitre_techniques": self._map_mitre(parsed_event.get("action")),
            "created_at": datetime.utcnow(),
        }

        # Add firewall-specific fields to metadata
        if parsed_event.get("rule"):
            normalized["metadata"]["rule"] = parsed_event["rule"]
        if parsed_event.get("bytes"):
            normalized["metadata"]["bytes"] = parsed_event["bytes"]
        if parsed_event.get("interface"):
            normalized["metadata"]["interface"] = parsed_event["interface"]
        if parsed_event.get("message"):
            normalized["metadata"]["original_message"] = parsed_event["message"]

        return self._set_defaults(self._ensure_required_fields(normalized))

    def _map_mitre(self, action: str) -> list:
        """Map firewall action to MITRE ATT&CK techniques."""
        if action in {"DENY", "DROP", "BLOCK", "REJECT"}:
            return ["T1021"]  # Remote Services (blocked connection attempt)
        elif action == "ALLOW":
            return []  # Allowed connections are not inherently suspicious
        return []

    def _generate_message(self, parsed_event: Dict[str, Any]) -> str:
        """Generate a human-readable message."""
        action = parsed_event.get("action", "Unknown action")
        src_ip = parsed_event.get("src_ip", "Unknown source")
        dst_ip = parsed_event.get("dst_ip", "Unknown destination")
        dst_port = parsed_event.get("dst_port", "Unknown port")
        protocol = parsed_event.get("protocol", "Unknown protocol")

        return f"{action} {protocol} connection from {src_ip} to {dst_ip}:{dst_port}"
