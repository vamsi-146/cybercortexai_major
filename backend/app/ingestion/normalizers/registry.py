"""Normalizer registry for managing event normalizers."""

from typing import Dict, Optional
from .base import BaseNormalizer
from .windows import WindowsNormalizer
from .linux import LinuxNormalizer
from .firewall import FirewallNormalizer
from .json_normalizer import JsonNormalizer


class NormalizerRegistry:
    """Registry for managing and accessing event normalizers."""

    _normalizers: Dict[str, BaseNormalizer] = {
        "windows": WindowsNormalizer(),
        "linux": LinuxNormalizer(),
        "firewall": FirewallNormalizer(),
        "json": JsonNormalizer(),
    }

    @classmethod
    def get_normalizer(cls, source_type: str) -> Optional[BaseNormalizer]:
        """
        Get normalizer for a specific source type.

        Args:
            source_type: The type of log source (windows, linux, firewall, json)

        Returns:
            Normalizer instance or None if not found
        """
        return cls._normalizers.get(source_type.lower())

    @classmethod
    def register_normalizer(cls, source_type: str, normalizer: BaseNormalizer):
        """
        Register a new normalizer.

        Args:
            source_type: The source type key
            normalizer: The normalizer instance
        """
        cls._normalizers[source_type.lower()] = normalizer

    @classmethod
    def get_supported_source_types(cls) -> list:
        """Return list of supported source types."""
        return list(cls._normalizers.keys())

    @classmethod
    def get_all_normalizers(cls) -> Dict[str, BaseNormalizer]:
        """Return all registered normalizers."""
        return cls._normalizers.copy()
