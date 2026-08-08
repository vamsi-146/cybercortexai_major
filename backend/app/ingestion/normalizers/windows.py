"""Windows event normalizer."""

import uuid
from typing import Dict, Any
from datetime import datetime
from .base import BaseNormalizer


class WindowsNormalizer(BaseNormalizer):
    """Normalizer for Windows Security Events."""

    FIELD_MAPPINGS = {
        "TargetUserName": "username",
        "SubjectUserName": "username",
        "IpAddress": "src_ip",
        "IpPort": "src_port",
        "WorkstationName": "dst_ip",
        "NewProcessName": "process_name",
        "ProcessName": "process_name",
        "NewProcessId": "process_id",
        "ProcessId": "process_id",
        "ParentProcessName": "parent_process_name",
        "TargetGroupName": "group_name",
        "TargetDomainName": "group_domain",
        "TargetDomainName": "account_domain",
    }

    def normalize(self, parsed_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize Windows event to CyberCortex common model."""
        normalized = {
            "event_id": str(uuid.uuid4()),
            "timestamp": parsed_event.get("timestamp", datetime.utcnow()),
            "received_at": datetime.utcnow(),
            "source_type": "windows",
            "source_name": parsed_event.get("source_name", "Windows Security Log"),
            "source_product": "Windows Event Log",
            "event_type": parsed_event.get("event_type", "unknown"),
            "category": self._map_category(parsed_event.get("event_code")),
            "severity": parsed_event.get("severity", "low"),
            "message": self._generate_message(parsed_event),
            "src_ip": parsed_event.get("src_ip"),
            "src_port": parsed_event.get("src_port"),
            "dst_ip": parsed_event.get("dst_ip"),
            "dst_port": None,
            "protocol": None,
            "username": parsed_event.get("username"),
            "hostname": parsed_event.get("computer"),
            "device_id": parsed_event.get("computer"),
            "process_name": parsed_event.get("process_name"),
            "process_id": parsed_event.get("process_id"),
            "parent_process_name": parsed_event.get("parent_process_name"),
            "command_line": None,
            "file_path": parsed_event.get("process_name"),
            "file_hash": None,
            "action": self._map_action(parsed_event.get("event_code")),
            "outcome": None,
            "event_code": parsed_event.get("event_code"),
            "authentication_type": parsed_event.get("logon_type"),
            "resource": parsed_event.get("account_name"),
            "raw_event": parsed_event.get("raw_event"),
            "metadata": parsed_event.get("metadata", {}),
            "tags": [],
            "mitre_techniques": self._map_mitre(parsed_event.get("event_code")),
            "created_at": datetime.utcnow(),
        }

        # Add additional Windows-specific fields to metadata
        if parsed_event.get("account_domain"):
            normalized["metadata"]["account_domain"] = parsed_event["account_domain"]
        if parsed_event.get("subject_username"):
            normalized["metadata"]["subject_username"] = parsed_event["subject_username"]
        if parsed_event.get("subject_domain"):
            normalized["metadata"]["subject_domain"] = parsed_event["subject_domain"]

        return self._set_defaults(self._ensure_required_fields(normalized))

    def _map_category(self, event_code: str) -> str:
        """Map Windows event code to category."""
        category_map = {
            "4624": "authentication",
            "4625": "authentication",
            "4672": "privilege",
            "4688": "process",
            "4720": "account",
            "4728": "account",
            "4732": "account",
            "4740": "authentication",
            "4768": "authentication",
            "4769": "authentication",
            "4776": "authentication",
        }
        return category_map.get(event_code, "unknown")

    def _map_action(self, event_code: str) -> str:
        """Map Windows event code to action."""
        action_map = {
            "4624": "login_success",
            "4625": "login_failure",
            "4672": "privilege_escalation",
            "4688": "process_created",
            "4720": "account_created",
            "4728": "group_member_added",
            "4732": "group_member_added",
            "4740": "account_locked",
            "4768": "kerberos_tgt_requested",
            "4769": "kerberos_service_ticket_requested",
            "4776": "credential_validation",
        }
        return action_map.get(event_code, "unknown")

    def _map_mitre(self, event_code: str) -> list:
        """Map Windows event code to MITRE ATT&CK techniques."""
        mitre_map = {
            "4624": ["T1078", "T1110"],  # Valid Accounts, Brute Force
            "4625": ["T1110"],  # Brute Force
            "4672": ["T1068"],  # Privilege Escalation
            "4688": ["T1059"],  # Command and Scripting Interpreter
            "4720": ["T1136"],  # Create Account
            "4728": ["T1098"],  # Account Manipulation
            "4732": ["T1098"],  # Account Manipulation
            "4740": ["T1110"],  # Brute Force
            "4768": ["T1558"],  # Steal or Forge Kerberos Tickets
            "4769": ["T1558"],  # Steal or Forge Kerberos Tickets
            "4776": ["T1110"],  # Brute Force
        }
        return mitre_map.get(event_code, [])

    def _generate_message(self, parsed_event: Dict[str, Any]) -> str:
        """Generate a human-readable message."""
        event_type = parsed_event.get("event_type", "Unknown event")
        username = parsed_event.get("username", "Unknown user")
        computer = parsed_event.get("computer", "Unknown computer")
        return f"{event_type} for user {username} on {computer}"
