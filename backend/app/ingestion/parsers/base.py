"""Base parser interface for log ingestion."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime


class BaseParser(ABC):
    """Abstract base class for log parsers."""

    @abstractmethod
    def parse(self, raw_event: str, source_context: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Parse a raw log event into a structured format.

        Args:
            raw_event: The raw log line/string
            source_context: Additional context about the source (file name, source type, etc.)

        Returns:
            Parsed event dict or None if parsing fails
        """
        pass

    @abstractmethod
    def get_supported_event_codes(self) -> List[str]:
        """Return list of supported event codes/types for this parser."""
        pass

    def extract_timestamp(self, raw_event: str) -> Optional[datetime]:
        """
        Extract timestamp from raw event.
        Override in subclass for source-specific timestamp formats.
        """
        return None

    def validate_parsed_event(self, event: Dict[str, Any]) -> bool:
        """
        Validate that a parsed event has required fields.
        Override in subclass for source-specific validation.
        """
        return True
