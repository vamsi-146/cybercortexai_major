"""Event enrichment service for adding contextual information."""

import ipaddress
from typing import Dict, Any, List, Optional
from datetime import datetime


class EnrichmentService:
    """Service for enriching security events with contextual information."""

    # Private IP ranges
    PRIVATE_RANGES = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
    ]

    # Documentation IP ranges (RFC 5737)
    DOC_RANGES = [
        ipaddress.ip_network("192.0.2.0/24"),
        ipaddress.ip_network("198.51.100.0/24"),
        ipaddress.ip_network("203.0.113.0/24"),
    ]

    @staticmethod
    def enrich(event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich a security event with contextual information.

        Args:
            event: The normalized event

        Returns:
            Enriched event with additional context
        """
        enriched = event.copy()

        # Initialize enrichment metadata
        if "enrichment" not in enriched:
            enriched["enrichment"] = {}

        # Enrich IP addresses
        if event.get("src_ip"):
            enriched["enrichment"]["src_ip_type"] = EnrichmentService.classify_ip(event["src_ip"])

        if event.get("dst_ip"):
            enriched["enrichment"]["dst_ip_type"] = EnrichmentService.classify_ip(event["dst_ip"])

        # Extract entities
        entities = EnrichmentService.extract_entities(event)
        if entities:
            enriched["enrichment"]["entities"] = entities

        # Add geographic hint (placeholder for future TI integration)
        if event.get("src_ip"):
            geo_hint = EnrichmentService.get_geo_hint(event["src_ip"])
            if geo_hint:
                enriched["enrichment"]["geo_hint"] = geo_hint

        return enriched

    @staticmethod
    def classify_ip(ip_str: str) -> str:
        """
        Classify an IP address.

        Args:
            ip_str: IP address string

        Returns:
            Classification: private, public, loopback, multicast, reserved, documentation
        """
        try:
            ip = ipaddress.ip_address(ip_str)

            if ip.is_loopback:
                return "loopback"
            elif ip.is_multicast:
                return "multicast"
            elif ip.is_private:
                return "private"
            elif ip.is_reserved:
                return "reserved"
            else:
                # Check if it's a documentation IP
                for doc_range in EnrichmentService.DOC_RANGES:
                    if ip in doc_range:
                        return "documentation"
                return "public"

        except ValueError:
            return "invalid"

    @staticmethod
    def extract_entities(event: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Extract security entities from an event.

        Args:
            event: The normalized event

        Returns:
            Dictionary of entity types to values
        """
        entities = {}

        # Users
        if event.get("username"):
            entities["users"] = [event["username"]]

        # Hosts
        hosts = []
        if event.get("hostname"):
            hosts.append(event["hostname"])
        if event.get("device_id") and event.get("device_id") not in hosts:
            hosts.append(event["device_id"])
        if hosts:
            entities["hosts"] = hosts

        # IPs
        ips = []
        if event.get("src_ip"):
            ips.append(event["src_ip"])
        if event.get("dst_ip") and event["dst_ip"] not in ips:
            ips.append(event["dst_ip"])
        if ips:
            entities["ips"] = ips

        # Processes
        processes = []
        if event.get("process_name"):
            processes.append(event["process_name"])
        if event.get("parent_process_name") and event["parent_process_name"] not in processes:
            processes.append(event["parent_process_name"])
        if processes:
            entities["processes"] = processes

        # Files
        if event.get("file_path"):
            entities["files"] = [event["file_path"]]

        # File hashes
        if event.get("file_hash"):
            entities["file_hashes"] = [event["file_hash"]]

        return entities

    @staticmethod
    def get_geo_hint(ip_str: str) -> Optional[str]:
        """
        Get geographic hint for an IP address.

        For Phase 3, this is a placeholder.
        Future phases can integrate with threat intelligence APIs.

        Args:
            ip_str: IP address string

        Returns:
            Geographic hint or None
        """
        # Phase 3: No external TI integration
        # Return None for all IPs
        return None

    @staticmethod
    def is_internal_network(ip_str: str) -> bool:
        """
        Check if an IP is from internal network.

        Args:
            ip_str: IP address string

        Returns:
            True if internal, False otherwise
        """
        classification = EnrichmentService.classify_ip(ip_str)
        return classification in {"private", "loopback"}

    @staticmethod
    def is_external_network(ip_str: str) -> bool:
        """
        Check if an IP is from external network.

        Args:
            ip_str: IP address string

        Returns:
            True if external, False otherwise
        """
        classification = EnrichmentService.classify_ip(ip_str)
        return classification == "public"
