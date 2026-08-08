"""Base detection rule interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class BaseDetectionRule(ABC):
    """Abstract base class for detection rules."""

    def __init__(self):
        self.rule_id = self.__class__.__name__
        self.name = ""
        self.description = ""
        self.enabled = True
        self.severity = "medium"
        self.source_types = []
        self.event_types = []
        self.mitre_techniques = []
        self.threshold = None
        self.time_window_seconds = 300

    @abstractmethod
    async def evaluate(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Evaluate if the event triggers this detection rule.

        Args:
            event: The normalized event
            context: Additional context (correlated events, etc.)

        Returns:
            Detection result dict if rule triggers, None otherwise
        """
        pass

    def check_source_type(self, event: Dict[str, Any]) -> bool:
        """Check if event source type is supported by this rule."""
        if not self.source_types:
            return True
        return event.get("source_type") in self.source_types

    def check_event_type(self, event: Dict[str, Any]) -> bool:
        """Check if event type is supported by this rule."""
        if not self.event_types:
            return True
        return event.get("event_type") in self.event_types

    def create_detection_result(
        self,
        event: Dict[str, Any],
        context: Dict[str, Any],
        reason: str,
        evidence: List[str]
    ) -> Dict[str, Any]:
        """
        Create a standardized detection result.

        Args:
            event: The triggering event
            context: Evaluation context
            reason: Why the rule triggered
            evidence: List of evidence strings

        Returns:
            Detection result dict
        """
        return {
            "rule_id": self.rule_id,
            "rule_name": self.name,
            "description": self.description,
            "severity": self.severity,
            "mitre_techniques": self.mitre_techniques,
            "triggering_event_id": event.get("event_id"),
            "triggering_event_timestamp": event.get("timestamp"),
            "reason": reason,
            "evidence": evidence,
            "correlated_event_ids": context.get("correlated_event_ids", []),
            "threshold_used": self.threshold,
            "time_window_seconds": self.time_window_seconds,
            "detection_timestamp": datetime.utcnow(),
        }
