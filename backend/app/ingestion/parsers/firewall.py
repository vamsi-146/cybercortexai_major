"""Firewall and network security log parser."""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseParser


class FirewallParser(BaseParser):
    """Parser for firewall and network security logs."""

    # Common firewall log patterns
    PATTERNS = {
        "standard": re.compile(
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})\s+(\w+)\s+([\d.]+):(\d+)\s+->\s+([\d.]+):(\d+)\s+(\w+)\s+(.+)'
        ),
        "cisco": re.compile(
            r'(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}):\s+(\w+):\s+([\d.]+)\((\d+)\)\s+->\s+([\d.]+)\((\d+)\)'
        ),
        "simple": re.compile(
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})\s+([\d.]+)\s+(\d+)\s+([\d.]+)\s+(\d+)\s+(\w+)\s+(\w+)'
        ),
    }

    SUPPORTED_ACTIONS = {"ALLOW", "DENY", "DROP", "BLOCK", "REJECT"}

    def get_supported_event_codes(self) -> List[str]:
        return list(self.PATTERNS.keys())

    def parse(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse firewall log line."""
        try:
            # Try different patterns
            for pattern_name, pattern in self.PATTERNS.items():
                match = pattern.search(raw_event)
                if match:
                    return self._parse_with_pattern(raw_event, match, pattern_name, source_context)

            # Try JSON format
            if raw_event.strip().startswith('{'):
                return self._parse_json(raw_event, source_context)

            return None

        except Exception:
            return None

    def _parse_with_pattern(self, raw_event: str, match: re.Match, pattern_name: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse using matched pattern."""
        if pattern_name == "standard":
            return self._parse_standard_format(raw_event, match, source_context)
        elif pattern_name == "cisco":
            return self._parse_cisco_format(raw_event, match, source_context)
        elif pattern_name == "simple":
            return self._parse_simple_format(raw_event, match, source_context)
        return None

    def _parse_standard_format(self, raw_event: str, match: re.Match, source_context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse standard firewall log format."""
        timestamp_str, action, src_ip, src_port, dst_ip, dst_port, protocol, message = match.groups()

        return {
            "timestamp": self._parse_timestamp(timestamp_str),
            "source_type": "firewall",
            "source_name": source_context.get("source_name", "Firewall Log"),
            "event_type": "network_connection",
            "event_code": "FW_" + action.upper(),
            "action": action.upper(),
            "src_ip": src_ip,
            "src_port": int(src_port) if src_port.isdigit() else None,
            "dst_ip": dst_ip,
            "dst_port": int(dst_port) if dst_port.isdigit() else None,
            "protocol": protocol.lower(),
            "message": message,
            "raw_event": raw_event,
            "severity": self._map_severity(action.upper()),
        }

    def _parse_cisco_format(self, raw_event: str, match: re.Match, source_context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Cisco ASA-like format."""
        timestamp_str, action, src_ip, src_port, dst_ip, dst_port = match.groups()

        return {
            "timestamp": self._parse_cisco_timestamp(timestamp_str),
            "source_type": "firewall",
            "source_name": source_context.get("source_name", "Cisco Firewall"),
            "event_type": "network_connection",
            "event_code": "FW_" + action.upper(),
            "action": action.upper(),
            "src_ip": src_ip,
            "src_port": int(src_port) if src_port.isdigit() else None,
            "dst_ip": dst_ip,
            "dst_port": int(dst_port) if dst_port.isdigit() else None,
            "raw_event": raw_event,
            "severity": self._map_severity(action.upper()),
        }

    def _parse_simple_format(self, raw_event: str, match: re.Match, source_context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse simple space-separated format."""
        timestamp_str, src_ip, src_port, dst_ip, dst_port, protocol, action = match.groups()

        return {
            "timestamp": self._parse_timestamp(timestamp_str),
            "source_type": "firewall",
            "source_name": source_context.get("source_name", "Firewall Log"),
            "event_type": "network_connection",
            "event_code": "FW_" + action.upper(),
            "action": action.upper(),
            "src_ip": src_ip,
            "src_port": int(src_port) if src_port.isdigit() else None,
            "dst_ip": dst_ip,
            "dst_port": int(dst_port) if dst_port.isdigit() else None,
            "protocol": protocol.lower(),
            "raw_event": raw_event,
            "severity": self._map_severity(action.upper()),
        }

    def _parse_json(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse JSON-formatted firewall log."""
        import json

        event_data = json.loads(raw_event)

        action = event_data.get("action", event_data.get("disposition", "UNKNOWN")).upper()
        if action not in self.SUPPORTED_ACTIONS:
            action = "UNKNOWN"

        timestamp = event_data.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = self._parse_timestamp(timestamp)
        else:
            timestamp = datetime.utcnow()

        return {
            "timestamp": timestamp,
            "source_type": "firewall",
            "source_name": source_context.get("source_name", "Firewall Log"),
            "event_type": "network_connection",
            "event_code": "FW_" + action,
            "action": action,
            "src_ip": event_data.get("src_ip", event_data.get("source_ip")),
            "src_port": event_data.get("src_port", event_data.get("source_port")),
            "dst_ip": event_data.get("dst_ip", event_data.get("destination_ip")),
            "dst_port": event_data.get("dst_port", event_data.get("destination_port")),
            "protocol": event_data.get("protocol", event_data.get("proto")),
            "rule": event_data.get("rule", event_data.get("rule_id")),
            "bytes": event_data.get("bytes"),
            "interface": event_data.get("interface"),
            "raw_event": raw_event,
            "severity": self._map_severity(action),
        }

    def _parse_timestamp(self, time_str: str) -> datetime:
        """Parse timestamp string."""
        formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S.%f",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(time_str, fmt)
            except:
                continue
        return datetime.utcnow()

    def _parse_cisco_timestamp(self, time_str: str) -> datetime:
        """Parse Cisco syslog timestamp format."""
        try:
            current_year = datetime.utcnow().year
            return datetime.strptime(f"{current_year} {time_str}", "%Y %b %d %H:%M:%S")
        except:
            return datetime.utcnow()

    def _map_severity(self, action: str) -> str:
        """Map firewall action to CyberCortex severity."""
        if action in {"DENY", "DROP", "BLOCK", "REJECT"}:
            return "medium"
        elif action == "ALLOW":
            return "low"
        else:
            return "low"
