"""Linux event normalizer."""

import uuid
from typing import Dict, Any
from datetime import datetime
from .base import BaseNormalizer


class LinuxNormalizer(BaseNormalizer):
    """Normalizer for Linux authentication and system logs."""

    def normalize(self, parsed_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Linux event to CyberCortex common model."""
        normalized = {
            "event_id": str(uuid.uuid4()),
            "timestamp": parsed_event.get("timestamp", datetime.utcnow()),
            "received_at": datetime.utcnow(),
            "source_type": "linux",
            "source_name": parsed_event.get("source_name", "Linux Auth Log"),
            "source_product": "Linux Syslog",
            "event_type": parsed_event.get("event_type", "unknown"),
            "category": self._map_category(parsed_event.get("event_type")),
            "severity": parsed_event.get("severity", "low"),
            "message": self._generate_message(parsed_event),
            "src_ip": parsed_event.get("src_ip"),
            "src_port": parsed_event.get("src_port"),
            "dst_ip": None,
            "dst_port": None,
            "protocol": None,
            "username": parsed_event.get("username"),
            "hostname": parsed_event.get("hostname"),
            "device_id": parsed_event.get("hostname"),
            "process_name": parsed_event.get("process"),
            "process_id": None,
            "parent_process_name": None,
            "command_line": parsed_event.get("command_line"),
            "file_path": None,
            "file_hash": None,
            "action": parsed_event.get("action"),
            "outcome": None,
            "event_code": parsed_event.get("event_code"),
            "authentication_type": parsed_event.get("auth_method"),
            "resource": None,
            "raw_event": parsed_event.get("raw_event"),
            "metadata": {},
            "tags": [],
            "mitre_techniques": self._map_mitre(parsed_event.get("event_type")),
            "created_at": datetime.utcnow(),
        }

        # Add Linux-specific fields to metadata
        if parsed_event.get("account"):
            normalized["metadata"]["account"] = parsed_event["account"]

        return self._set_defaults(self._ensure_required_fields(normalized))

    def _map_category(self, event_type: str) -> str:
        """Map Linux event type to category."""
        category_map = {
            "ssh_success": "authentication",
            "ssh_failure": "authentication",
            "ssh_invalid_user": "authentication",
            "sudo_success": "privilege",
            "sudo_failure": "privilege",
            "session_opened": "session",
            "session_closed": "session",
            "account_locked": "authentication",
        }
        return category_map.get(event_type, "unknown")

    def _map_mitre(self, event_type: str) -> list:
        """Map Linux event type to MITRE ATT&CK techniques."""
        mitre_map = {
            "ssh_success": ["T1078", "T1021"],  # Valid Accounts, Remote Services
            "ssh_failure": ["T1110"],  # Brute Force
            "ssh_invalid_user": ["T1110"],  # Brute Force
            "sudo_success": ["T1548"],  # Abuse Elevation Control Mechanism
            "sudo_failure": ["T1548"],  # Abuse Elevation Control Mechanism
            "account_locked": ["T1110"],  # Brute Force
        }
        return mitre_map.get(event_type, [])

    def _generate_message(self, parsed_event: Dict[str, Any]) -> str:
        """Generate a human-readable message."""
        event_type = parsed_event.get("event_type", "Unknown event")
        username = parsed_event.get("username", "Unknown user")
        hostname = parsed_event.get("hostname", "Unknown host")
        src_ip = parsed_event.get("src_ip", "")

        if src_ip:
            return f"{event_type} for user {username} from {src_ip} on {hostname}"
        return f"{event_type} for user {username} on {hostname}"
