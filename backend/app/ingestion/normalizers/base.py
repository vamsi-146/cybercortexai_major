"""Base normalizer interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseNormalizer(ABC):
    """Abstract base class for event normalizers."""

    @abstractmethod
    def normalize(self, parsed_event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Normalize a parsed event to the CyberCortex common event model.

        Args:
            parsed_event: The parsed event from a parser

        Returns:
            Normalized event dict
        """
        pass

    def _ensure_required_fields(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure all required fields are present."""
        required_fields = ["event_id", "timestamp", "source_type", "event_type"]
        for field in required_fields:
            if field not in event:
                event[field] = None
        return event

    def _set_defaults(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Set default values for optional fields."""
        defaults = {
            "category": "unknown",
            "severity": "low",
            "received_at": event.get("timestamp"),
            "tags": [],
            "metadata": {},
        }
        for key, value in defaults.items():
            if key not in event or event[key] is None:
                event[key] = value
        return event
