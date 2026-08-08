"""Windows Security Event Log parser."""

import re
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseParser


class WindowsParser(BaseParser):
    """Parser for Windows Security Event logs."""

    # Supported Windows Security Event IDs
    SUPPORTED_EVENTS = {
        "4624": "An account was successfully logged on",
        "4625": "An account failed to log on",
        "4672": "Special privileges assigned to new logon",
        "4688": "A new process has been created",
        "4720": "A user account was created",
        "4728": "A member was added to a security-enabled global group",
        "4732": "A member was added to a security-enabled local group",
        "4740": "A user account was locked out",
        "4768": "A Kerberos authentication ticket (TGT) was requested",
        "4769": "A Kerberos service ticket was requested",
        "4776": "The computer attempted to validate the credentials for an account",
    }

    def get_supported_event_codes(self) -> List[str]:
        return list(self.SUPPORTED_EVENTS.keys())

    def parse(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse Windows Security Event log.

        Supports both XML format (from Event Viewer) and JSON format.
        """
        try:
            # Try JSON format first
            if raw_event.strip().startswith('{'):
                return self._parse_json(raw_event, source_context)
            # Try XML format
            elif '<Event' in raw_event:
                return self._parse_xml(raw_event, source_context)
            # Try simple text format
            else:
                return self._parse_text(raw_event, source_context)
        except Exception:
            return None

    def _parse_json(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse JSON-formatted Windows event."""
        event_data = json.loads(raw_event)

        event_id = str(event_data.get("EventID") or event_data.get("System", {}).get("EventID"))
        if event_id not in self.SUPPORTED_EVENTS:
            return None

        timestamp = self._extract_timestamp_json(event_data)
        system = event_data.get("System", {})
        event = event_data.get("EventData", {})

        parsed = {
            "event_id": event_id,
            "timestamp": timestamp,
            "source_type": "windows",
            "source_name": source_context.get("source_name", "Windows Security Log"),
            "event_type": self.SUPPORTED_EVENTS.get(event_id, "Unknown"),
            "event_code": event_id,
            "computer": system.get("Computer"),
            "username": event.get("TargetUserName") or event.get("SubjectUserName"),
            "src_ip": event.get("IpAddress"),
            "src_port": event.get("IpPort"),
            "dst_ip": event.get("WorkstationName"),
            "logon_type": event.get("LogonType"),
            "logon_process": event.get("ProcessName"),
            "process_name": event.get("NewProcessName") or event.get("ProcessName"),
            "process_id": event.get("NewProcessId") or event.get("ProcessId"),
            "parent_process_name": event.get("ParentProcessName"),
            "account_name": event.get("TargetUserName"),
            "account_domain": event.get("TargetDomainName"),
            "subject_username": event.get("SubjectUserName"),
            "subject_domain": event.get("SubjectDomainName"),
            "group_name": event.get("TargetGroupName"),
            "group_domain": event.get("TargetDomainName"),
            "failure_reason": event.get("FailureReason"),
            "status": event.get("Status"),
            "sub_status": event.get("SubStatus"),
            "raw_event": raw_event,
            "metadata": {
                "provider": system.get("Provider", {}).get("Name"),
                "channel": system.get("Channel"),
                "level": system.get("Level"),
                "task": system.get("Task"),
                "keywords": system.get("Keywords"),
            }
        }

        # Determine severity based on event ID
        parsed["severity"] = self._map_severity(event_id)

        return parsed

    def _parse_xml(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse XML-formatted Windows event (simplified)."""
        # Extract EventID using regex
        event_id_match = re.search(r'<EventID>(\d+)</EventID>', raw_event)
        if not event_id_match:
            return None

        event_id = event_id_match.group(1)
        if event_id not in self.SUPPORTED_EVENTS:
            return None

        timestamp = self._extract_timestamp_xml(raw_event)

        # Extract common fields using regex
        computer = self._extract_xml_field(raw_event, "Computer")
        username = self._extract_xml_field(raw_event, "TargetUserName") or self._extract_xml_field(raw_event, "SubjectUserName")
        src_ip = self._extract_xml_field(raw_event, "IpAddress")
        process_name = self._extract_xml_field(raw_event, "NewProcessName") or self._extract_xml_field(raw_event, "ProcessName")

        parsed = {
            "event_id": event_id,
            "timestamp": timestamp,
            "source_type": "windows",
            "source_name": source_context.get("source_name", "Windows Security Log"),
            "event_type": self.SUPPORTED_EVENTS.get(event_id, "Unknown"),
            "event_code": event_id,
            "computer": computer,
            "username": username,
            "src_ip": src_ip,
            "process_name": process_name,
            "raw_event": raw_event,
            "severity": self._map_severity(event_id),
        }

        return parsed

    def _parse_text(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse simple text format Windows event."""
        # This is a fallback for non-standard text formats
        # Try to extract event ID
        event_id_match = re.search(r'Event ID:\s*(\d+)', raw_event)
        if not event_id_match:
            return None

        event_id = event_id_match.group(1)
        if event_id not in self.SUPPORTED_EVENTS:
            return None

        return {
            "event_id": event_id,
            "timestamp": datetime.utcnow(),
            "source_type": "windows",
            "source_name": source_context.get("source_name", "Windows Security Log"),
            "event_type": self.SUPPORTED_EVENTS.get(event_id, "Unknown"),
            "event_code": event_id,
            "raw_event": raw_event,
            "severity": self._map_severity(event_id),
        }

    def _extract_timestamp_json(self, event_data: Dict[str, Any]) -> datetime:
        """Extract timestamp from JSON event."""
        time_str = event_data.get("System", {}).get("TimeCreated", {}).get("SystemTime")
        if time_str:
            try:
                return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            except:
                pass
        return datetime.utcnow()

    def _extract_timestamp_xml(self, raw_event: str) -> datetime:
        """Extract timestamp from XML event."""
        time_match = re.search(r'TimeCreated SystemTime="([^"]+)"', raw_event)
        if time_match:
            try:
                time_str = time_match.group(1)
                return datetime.fromisoformat(time_str.replace('Z', '+00:00'))
            except:
                pass
        return datetime.utcnow()

    def _extract_xml_field(self, xml: str, field_name: str) -> Optional[str]:
        """Extract a field value from XML."""
        match = re.search(f'<{field_name}[^>]*>([^<]+)</{field_name}>', xml)
        return match.group(1) if match else None

    def _map_severity(self, event_id: str) -> str:
        """Map Windows event ID to CyberCortex severity."""
        high_severity_events = {"4625", "4740", "4768", "4776"}  # Failed logon, lockout, Kerberos
        medium_severity_events = {"4672", "4720", "4728", "4732"}  # Privileges, account creation, group changes

        if event_id in high_severity_events:
            return "high"
        elif event_id in medium_severity_events:
            return "medium"
        else:
            return "low"
