"""Correlation engine for linking related security events."""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from app.database.mongodb import get_database


class CorrelationEngine:
    """Engine for correlating related security events."""

    # Default correlation windows (in seconds)
    DEFAULT_WINDOWS = {
        "short": 60,      # 1 minute
        "medium": 300,    # 5 minutes
        "long": 900,      # 15 minutes
        "extended": 1800, # 30 minutes
    }

    @staticmethod
    async def correlate_event(
        event: Dict[str, Any],
        window_seconds: int = 300
    ) -> Dict[str, Any]:
        """
        Correlate an event with historical events.

        Args:
            event: The normalized event to correlate
            window_seconds: Time window in seconds to look back

        Returns:
            Correlation result with related events and correlation score
        """
        db = await get_database()
        events_collection = db.security_events

        timestamp = event.get("timestamp", datetime.utcnow())
        window_start = timestamp - timedelta(seconds=window_seconds)

        # Build correlation queries based on event entities
        related_events = []

        # Correlate by username
        if event.get("username"):
            username_events = await events_collection.find({
                "username": event["username"],
                "timestamp": {"$gte": window_start, "$lte": timestamp},
                "event_id": {"$ne": event.get("event_id")}
            }).to_list(length=100)
            related_events.extend(username_events)

        # Correlate by source IP
        if event.get("src_ip"):
            src_ip_events = await events_collection.find({
                "src_ip": event["src_ip"],
                "timestamp": {"$gte": window_start, "$lte": timestamp},
                "event_id": {"$ne": event.get("event_id")}
            }).to_list(length=100)
            related_events.extend(src_ip_events)

        # Correlate by destination IP
        if event.get("dst_ip"):
            dst_ip_events = await events_collection.find({
                "dst_ip": event["dst_ip"],
                "timestamp": {"$gte": window_start, "$lte": timestamp},
                "event_id": {"$ne": event.get("event_id")}
            }).to_list(length=100)
            related_events.extend(dst_ip_events)

        # Correlate by hostname
        if event.get("hostname"):
            hostname_events = await events_collection.find({
                "hostname": event["hostname"],
                "timestamp": {"$gte": window_start, "$lte": timestamp},
                "event_id": {"$ne": event.get("event_id")}
            }).to_list(length=100)
            related_events.extend(hostname_events)

        # Correlate by device_id
        if event.get("device_id"):
            device_events = await events_collection.find({
                "device_id": event["device_id"],
                "timestamp": {"$gte": window_start, "$lte": timestamp},
                "event_id": {"$ne": event.get("event_id")}
            }).to_list(length=100)
            related_events.extend(device_events)

        # Correlate by MITRE technique
        if event.get("mitre_techniques"):
            mitre_events = await events_collection.find({
                "mitre_techniques": {"$in": event["mitre_techniques"]},
                "timestamp": {"$gte": window_start, "$lte": timestamp},
                "event_id": {"$ne": event.get("event_id")}
            }).to_list(length=100)
            related_events.extend(mitre_events)

        # Deduplicate events
        unique_events = CorrelationEngine._deduplicate_events(related_events)

        # Calculate correlation score
        correlation_score = CorrelationEngine._calculate_correlation_score(
            event, unique_events, window_seconds
        )

        # Identify correlation patterns
        patterns = CorrelationEngine._identify_patterns(event, unique_events)

        return {
            "correlated_event_ids": [e["event_id"] for e in unique_events],
            "correlation_count": len(unique_events),
            "correlation_score": correlation_score,
            "correlation_window_seconds": window_seconds,
            "patterns": patterns,
            "related_entities": CorrelationEngine._extract_related_entities(event, unique_events),
        }

    @staticmethod
    def _deduplicate_events(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate events from list."""
        seen_ids = set()
        unique = []
        for event in events:
            event_id = event.get("event_id")
            if event_id and event_id not in seen_ids:
                seen_ids.add(event_id)
                unique.append(event)
        return unique

    @staticmethod
    def _calculate_correlation_score(
        event: Dict[str, Any],
        related_events: List[Dict[str, Any]],
        window_seconds: int
    ) -> float:
        """
        Calculate correlation score (0-100).

        Higher score indicates stronger correlation.
        """
        if not related_events:
            return 0.0

        score = 0.0

        # Base score for having related events
        score += min(len(related_events) * 5, 30)  # Max 30 points for quantity

        # Time proximity bonus
        timestamp = event.get("timestamp", datetime.utcnow())
        for related in related_events:
            related_time = related.get("timestamp", datetime.utcnow())
            time_diff = abs((timestamp - related_time).total_seconds())
            if time_diff < 60:  # Within 1 minute
                score += 5
            elif time_diff < 300:  # Within 5 minutes
                score += 3
            elif time_diff < 900:  # Within 15 minutes
                score += 1

        # Entity overlap bonus
        entities = CorrelationEngine._extract_entities(event)
        for related in related_events:
            related_entities = CorrelationEngine._extract_entities(related)
            overlap = len(set(entities) & set(related_entities))
            score += min(overlap * 2, 10)  # Max 10 points per event

        # MITRE technique overlap
        event_mitre = set(event.get("mitre_techniques", []))
        for related in related_events:
            related_mitre = set(related.get("mitre_techniques", []))
            if event_mitre & related_mitre:
                score += 5

        # Severity weight
        event_severity = event.get("severity", "low")
        if event_severity == "critical":
            score *= 1.2
        elif event_severity == "high":
            score *= 1.1

        return min(score, 100.0)

    @staticmethod
    def _identify_patterns(
        event: Dict[str, Any],
        related_events: List[Dict[str, Any]]
    ) -> List[str]:
        """Identify correlation patterns in related events."""
        patterns = []

        # Check for authentication pattern
        auth_events = [e for e in related_events if e.get("category") == "authentication"]
        if auth_events:
            failures = [e for e in auth_events if e.get("action") in ["login_failure", "account_locked"]]
            successes = [e for e in auth_events if e.get("action") == "login_success"]
            if failures and successes:
                patterns.append("auth_success_after_failures")
            elif len(failures) >= 3:
                patterns.append("repeated_auth_failures")

        # Check for privilege escalation pattern
        privilege_events = [e for e in related_events if e.get("category") == "privilege"]
        if privilege_events:
            patterns.append("privilege_activity")

        # Check for network scan pattern
        network_events = [e for e in related_events if e.get("category") == "network"]
        unique_dst_ports = set(e.get("dst_port") for e in network_events if e.get("dst_port"))
        if len(unique_dst_ports) >= 10:
            patterns.append("port_scan")

        # Check for process execution pattern
        process_events = [e for e in related_events if e.get("category") == "process"]
        if process_events:
            patterns.append("process_activity")

        return patterns

    @staticmethod
    def _extract_entities(event: Dict[str, Any]) -> List[str]:
        """Extract entity identifiers from event."""
        entities = []
        if event.get("username"):
            entities.append(f"user:{event['username']}")
        if event.get("src_ip"):
            entities.append(f"ip:{event['src_ip']}")
        if event.get("dst_ip"):
            entities.append(f"ip:{event['dst_ip']}")
        if event.get("hostname"):
            entities.append(f"host:{event['hostname']}")
        if event.get("device_id"):
            entities.append(f"device:{event['device_id']}")
        if event.get("process_name"):
            entities.append(f"process:{event['process_name']}")
        return entities

    @staticmethod
    def _extract_related_entities(
        event: Dict[str, Any],
        related_events: List[Dict[str, Any]]
    ) -> Dict[str, List[str]]:
        """Extract all related entities from event and related events."""
        all_entities = CorrelationEngine._extract_entities(event)
        for related in related_events:
            all_entities.extend(CorrelationEngine._extract_entities(related))

        # Organize by entity type
        organized = {}
        for entity in all_entities:
            entity_type, entity_value = entity.split(":", 1)
            if entity_type not in organized:
                organized[entity_type] = []
            if entity_value not in organized[entity_type]:
                organized[entity_type].append(entity_value)

        return organized
