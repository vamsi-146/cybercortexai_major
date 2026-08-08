"""Parser registry for managing log parsers."""

from typing import Dict, Optional
from .base import BaseParser
from .windows import WindowsParser
from .linux import LinuxParser
from .firewall import FirewallParser
from .json_parser import JsonParser


class ParserRegistry:
    """Registry for managing and accessing log parsers."""

    _parsers: Dict[str, BaseParser] = {
        "windows": WindowsParser(),
        "linux": LinuxParser(),
        "firewall": FirewallParser(),
        "json": JsonParser(),
    }

    @classmethod
    def get_parser(cls, source_type: str) -> Optional[BaseParser]:
        """
        Get parser for a specific source type.

        Args:
            source_type: The type of log source (windows, linux, firewall, json)

        Returns:
            Parser instance or None if not found
        """
        return cls._parsers.get(source_type.lower())

    @classmethod
    def register_parser(cls, source_type: str, parser: BaseParser):
        """
        Register a new parser.

        Args:
            source_type: The source type key
            parser: The parser instance
        """
        cls._parsers[source_type.lower()] = parser

    @classmethod
    def get_supported_source_types(cls) -> list:
        """Return list of supported source types."""
        return list(cls._parsers.keys())

    @classmethod
    def get_all_parsers(cls) -> Dict[str, BaseParser]:
        """Return all registered parsers."""
        return cls._parsers.copy()
