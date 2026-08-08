"""Linux authentication and system log parser."""

import re
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseParser


class LinuxParser(BaseParser):
    """Parser for Linux auth.log and secure logs."""

    # Common Linux log patterns
    PATTERNS = {
        "ssh_success": re.compile(
            r'Accepted (\w+) for (\w+) from ([\d.]+) port (\d+)'
        ),
        "ssh_failure": re.compile(
            r'Failed (\w+) for (?:invalid user )?(\w+) from ([\d.]+) port (\d+)'
        ),
        "ssh_invalid_user": re.compile(
            r'Invalid user (\w+) from ([\d.]+)'
        ),
        "sudo_success": re.compile(
            r'(\w+) : (\w+) ; COMMAND=(.+)'
        ),
        "sudo_failure": re.compile(
            r'(\w+) : (\w+) ; command not allowed ; COMMAND=(.+)'
        ),
        "session_opened": re.compile(
            r'session opened for user (\w+)'
        ),
        "session_closed": re.compile(
            r'session closed for user (\w+)'
        ),
        "account_locked": re.compile(
            r'pam_unix\([^)]+\): authentication failure'
        ),
    }

    def get_supported_event_codes(self) -> List[str]:
        return list(self.PATTERNS.keys())

    def parse(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Parse Linux log line."""
        try:
            timestamp = self._extract_timestamp(raw_event)
            if not timestamp:
                return None

            event_type = self._detect_event_type(raw_event)
            if not event_type:
                return None

            parsed = {
                "timestamp": timestamp,
                "source_type": "linux",
                "source_name": source_context.get("source_name", "Linux Auth Log"),
                "event_type": event_type,
                "event_code": event_type,
                "hostname": self._extract_hostname(raw_event),
                "process": self._extract_process(raw_event),
                "raw_event": raw_event,
                "severity": self._map_severity(event_type),
            }

            # Add event-specific fields
            self._add_event_specific_fields(parsed, raw_event, event_type)

            return parsed

        except Exception:
            return None

    def _extract_timestamp(self, raw_event: str) -> Optional[datetime]:
        """Extract timestamp from Linux log line."""
        # Try common formats: "Jan 15 10:30:45" or "2024-01-15T10:30:45"
        patterns = [
            r'^(\w{3}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2})',
            r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})',
            r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})',
        ]

        for pattern in patterns:
            match = re.search(pattern, raw_event)
            if match:
                time_str = match.group(1)
                try:
                    # Try parsing with year if present
                    if '-' in time_str:
                        return datetime.fromisoformat(time_str)
                    else:
                        # Assume current year for syslog format
                        current_year = datetime.utcnow().year
                        return datetime.strptime(f"{current_year} {time_str}", "%Y %b %d %H:%M:%S")
                except:
                    continue

        return None

    def _detect_event_type(self, raw_event: str) -> Optional[str]:
        """Detect the type of Linux event."""
        for event_type, pattern in self.PATTERNS.items():
            if pattern.search(raw_event):
                return event_type
        return None

    def _extract_hostname(self, raw_event: str) -> Optional[str]:
        """Extract hostname from log line."""
        match = re.search(r'\s(\S+)\s+(?:sshd|sudo|systemd-login):', raw_event)
        return match.group(1) if match else None

    def _extract_process(self, raw_event: str) -> Optional[str]:
        """Extract process name from log line."""
        match = re.search(r'(\w+)(?:\[\d+\])?:', raw_event)
        return match.group(1) if match else None

    def _add_event_specific_fields(self, parsed: Dict[str, Any], raw_event: str, event_type: str):
        """Add fields specific to the event type."""
        if event_type == "ssh_success":
            match = self.PATTERNS["ssh_success"].search(raw_event)
            if match:
                parsed["auth_method"] = match.group(1)
                parsed["username"] = match.group(2)
                parsed["src_ip"] = match.group(3)
                parsed["src_port"] = match.group(4)
                parsed["action"] = "login_success"

        elif event_type == "ssh_failure":
            match = self.PATTERNS["ssh_failure"].search(raw_event)
            if match:
                parsed["auth_method"] = match.group(1)
                parsed["username"] = match.group(2)
                parsed["src_ip"] = match.group(3)
                parsed["src_port"] = match.group(4)
                parsed["action"] = "login_failure"

        elif event_type == "ssh_invalid_user":
            match = self.PATTERNS["ssh_invalid_user"].search(raw_event)
            if match:
                parsed["username"] = match.group(1)
                parsed["src_ip"] = match.group(2)
                parsed["action"] = "invalid_user"

        elif event_type in ["sudo_success", "sudo_failure"]:
            match = self.PATTERNS["sudo_success"].search(raw_event) or self.PATTERNS["sudo_failure"].search(raw_event)
            if match:
                parsed["username"] = match.group(1)
                parsed["account"] = match.group(2)
                parsed["command_line"] = match.group(3)
                parsed["action"] = "sudo_execution"

        elif event_type == "session_opened":
            match = self.PATTERNS["session_opened"].search(raw_event)
            if match:
                parsed["username"] = match.group(1)
                parsed["action"] = "session_open"

        elif event_type == "session_closed":
            match = self.PATTERNS["session_closed"].search(raw_event)
            if match:
                parsed["username"] = match.group(1)
                parsed["action"] = "session_close"

    def _map_severity(self, event_type: str) -> str:
        """Map Linux event type to CyberCortex severity."""
        high_severity = ["ssh_failure", "ssh_invalid_user", "account_locked"]
        medium_severity = ["sudo_failure"]

        if event_type in high_severity:
            return "high"
        elif event_type in medium_severity:
            return "medium"
        else:
            return "low"
