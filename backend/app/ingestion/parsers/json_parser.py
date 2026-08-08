"""Generic JSON event parser for normalized or semi-normalized events."""

import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from .base import BaseParser


class JsonParser(BaseParser):
    """Parser for generic JSON security events."""

    def get_supported_event_codes(self) -> List[str]:
        return ["json", "generic"]

    def parse(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse JSON-formatted security event.

        Supports both normalized and semi-normalized JSON events.
        """
        try:
            event_data = json.loads(raw_event)

            # Normalize common field names
            parsed = {
                "timestamp": self._extract_timestamp(event_data),
                "source_type": event_data.get("source_type", source_context.get("source_type", "json")),
                "source_name": event_data.get("source_name", source_context.get("source_name", "Generic JSON")),
                "event_type": event_data.get("event_type", event_data.get("type", "generic")),
                "event_code": event_data.get("event_code", event_data.get("code", "GENERIC")),
                "category": event_data.get("category"),
                "severity": self._normalize_severity(event_data.get("severity")),
                "message": event_data.get("message", event_data.get("description")),
                "src_ip": self._normalize_ip(event_data, "src_ip", "source_ip", "ip_address"),
                "src_port": event_data.get("src_port", event_data.get("source_port")),
                "dst_ip": self._normalize_ip(event_data, "dst_ip", "destination_ip", "target_ip"),
                "dst_port": event_data.get("dst_port", event_data.get("destination_port", "target_port")),
                "protocol": event_data.get("protocol", event_data.get("proto")),
                "username": self._normalize_username(event_data),
                "hostname": event_data.get("hostname", event_data.get("host", event_data.get("device_name"))),
                "device_id": event_data.get("device_id", event_data.get("asset_id")),
                "process_name": event_data.get("process_name", event_data.get("process")),
                "process_id": event_data.get("process_id", event_data.get("pid")),
                "parent_process_name": event_data.get("parent_process_name", event_data.get("parent_process")),
                "command_line": event_data.get("command_line", event_data.get("cmdline")),
                "file_path": event_data.get("file_path", event_data.get("filepath")),
                "file_hash": event_data.get("file_hash", event_data.get("hash")),
                "action": event_data.get("action"),
                "outcome": event_data.get("outcome", event_data.get("result")),
                "resource": event_data.get("resource"),
                "tags": event_data.get("tags", []),
                "raw_event": raw_event,
                "metadata": self._extract_metadata(event_data),
            }

            # Remove None values
            parsed = {k: v for k, v in parsed.items() if v is not None}

            return parsed

        except json.JSONDecodeError:
            return None
        except Exception:
            return None

    def _extract_timestamp(self, event_data: Dict[str, Any]) -> datetime:
        """Extract and parse timestamp from event data."""
        time_fields = ["timestamp", "time", "datetime", "created_at", "event_time", "@timestamp"]
        for field in time_fields:
            if field in event_data:
                time_str = event_data[field]
                try:
                    if isinstance(time_str, (int, float)):
                        # Unix timestamp
                        return datetime.fromtimestamp(time_str)
                    elif isinstance(time_str, str):
                        # ISO format or other
                        return self._parse_time_string(time_str)
                except:
                    continue
        return datetime.utcnow()

    def _parse_time_string(self, time_str: str) -> datetime:
        """Parse various time string formats."""
        formats = [
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%SZ",
            "%Y-%m-%dT%H:%M:%S.%f",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
        ]
        for fmt in formats:
            try:
                return datetime.strptime(time_str, fmt)
            except:
                continue
        return datetime.utcnow()

    def _normalize_severity(self, severity: Any) -> str:
        """Normalize severity to CyberCortex standard."""
        if not severity:
            return "low"

        severity_map = {
            "critical": "critical",
            "high": "high",
            "medium": "medium",
            "low": "low",
            "informational": "low",
            "info": "low",
            "warning": "medium",
            "warn": "medium",
            "error": "high",
            "fatal": "critical",
        }

        severity_lower = str(severity).lower()
        return severity_map.get(severity_lower, "low")

    def _normalize_ip(self, event_data: Dict[str, Any], *field_names) -> Optional[str]:
        """Extract IP address from various possible field names."""
        for field in field_names:
            if field in event_data:
                ip = event_data[field]
                if self._is_valid_ip(ip):
                    return ip
        return None

    def _is_valid_ip(self, ip: Any) -> bool:
        """Basic IP validation."""
        if not ip or not isinstance(ip, str):
            return False
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        try:
            return all(0 <= int(part) <= 255 for part in parts)
        except:
            return False

    def _normalize_username(self, event_data: Dict[str, Any]) -> Optional[str]:
        """Extract username from various possible field names."""
        username_fields = ["username", "user", "account", "principal", "actor", "subject"]
        for field in username_fields:
            if field in event_data:
                return str(event_data[field])
        return None

    def _extract_metadata(self, event_data: Dict[str, Any]) -> Dict[str, Any]:
        """Extract additional metadata from event."""
        # Fields that are not in the standard schema go to metadata
        standard_fields = {
            "timestamp", "source_type", "source_name", "event_type", "event_code",
            "category", "severity", "message", "src_ip", "src_port", "dst_ip",
            "dst_port", "protocol", "username", "hostname", "device_id",
            "process_name", "process_id", "parent_process_name", "command_line",
            "file_path", "file_hash", "action", "outcome", "resource", "tags",
        }

        metadata = {}
        for key, value in event_data.items():
            if key not in standard_fields and not key.startswith("_"):
                metadata[key] = value

        return metadata
