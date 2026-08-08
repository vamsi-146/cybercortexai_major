"""JSON event normalizer."""

import uuid
from typing import Dict, Any
from datetime import datetime
from .base import BaseNormalizer


class JsonNormalizer(BaseNormalizer):
    """Normalizer for generic JSON events (already partially normalized)."""

    def normalize(self, parsed_event: Dict[str, Any]) -> Dict[str, Any]:
        """Normalize JSON event to CyberCortex common model."""
        normalized = {
            "event_id": str(uuid.uuid4()),
            "timestamp": parsed_event.get("timestamp", datetime.utcnow()),
            "received_at": datetime.utcnow(),
            "source_type": parsed_event.get("source_type", "json"),
            "source_name": parsed_event.get("source_name", "Generic JSON"),
            "source_product": parsed_event.get("source_product", "Generic"),
            "event_type": parsed_event.get("event_type", "generic"),
            "category": parsed_event.get("category", "unknown"),
            "severity": parsed_event.get("severity", "low"),
            "message": parsed_event.get("message", "Generic security event"),
            "src_ip": parsed_event.get("src_ip"),
            "src_port": parsed_event.get("src_port"),
            "dst_ip": parsed_event.get("dst_ip"),
            "dst_port": parsed_event.get("dst_port"),
            "protocol": parsed_event.get("protocol"),
            "username": parsed_event.get("username"),
            "hostname": parsed_event.get("hostname"),
            "device_id": parsed_event.get("device_id"),
            "process_name": parsed_event.get("process_name"),
            "process_id": parsed_event.get("process_id"),
            "parent_process_name": parsed_event.get("parent_process_name"),
            "command_line": parsed_event.get("command_line"),
            "file_path": parsed_event.get("file_path"),
            "file_hash": parsed_event.get("file_hash"),
            "action": parsed_event.get("action"),
            "outcome": parsed_event.get("outcome"),
            "event_code": parsed_event.get("event_code"),
            "authentication_type": None,
            "resource": parsed_event.get("resource"),
            "raw_event": parsed_event.get("raw_event"),
            "metadata": parsed_event.get("metadata", {}),
            "tags": parsed_event.get("tags", []),
            "mitre_techniques": parsed_event.get("mitre_techniques", []),
            "created_at": datetime.utcnow(),
        }

        return self._set_defaults(self._ensure_required_fields(normalized))
