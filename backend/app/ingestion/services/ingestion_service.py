"""Ingestion service for orchestrating the event processing pipeline."""

import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from app.database.mongodb import get_database
from app.ingestion.parsers import ParserRegistry
from app.ingestion.normalizers import NormalizerRegistry
from app.enrichment.service import EnrichmentService
from app.correlation.engine import CorrelationEngine
from app.detection.engine.detection_engine import DetectionEngine
from app.services.alert_generation import AlertGenerationService
from app.incidents.grouping.service import IncidentGroupingService


class IngestionService:
    """Service for orchestrating the event ingestion pipeline."""

    def __init__(self):
        self.parser_registry = ParserRegistry()
        self.normalizer_registry = NormalizerRegistry()
        self.enrichment_service = EnrichmentService()
        self.correlation_engine = CorrelationEngine()
        self.detection_engine = DetectionEngine()
        self.alert_service = AlertGenerationService()
        self.incident_service = IncidentGroupingService()

    async def ingest_event(
        self,
        raw_event: str,
        source_type: str,
        source_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ingest a single raw event through the pipeline.

        Args:
            raw_event: The raw log line/string
            source_type: The type of log source (windows, linux, firewall, json)
            source_context: Additional context about the source

        Returns:
            Processing result with event ID, alerts, incidents, etc.
        """
        processing_result = {
            "received": 1,
            "parsed": 0,
            "normalized": 0,
            "enriched": 0,
            "stored": 0,
            "rejected": 0,
            "alerts_generated": 0,
            "incidents_created": 0,
            "errors": [],
        }

        try:
            # Step 1: Parse
            parser = self.parser_registry.get_parser(source_type)
            if not parser:
                processing_result["rejected"] = 1
                processing_result["errors"].append(f"No parser for source type: {source_type}")
                return processing_result

            parsed_event = parser.parse(raw_event, source_context)
            if not parsed_event:
                processing_result["rejected"] = 1
                processing_result["errors"].append("Parser returned None")
                return processing_result

            processing_result["parsed"] = 1

            # Step 2: Normalize
            normalizer = self.normalizer_registry.get_normalizer(source_type)
            if not normalizer:
                processing_result["rejected"] = 1
                processing_result["errors"].append(f"No normalizer for source type: {source_type}")
                return processing_result

            normalized_event = normalizer.normalize(parsed_event)
            processing_result["normalized"] = 1

            # Step 3: Enrich
            enriched_event = self.enrichment_service.enrich(normalized_event)
            processing_result["enriched"] = 1

            # Step 4: Store
            db = await get_database()
            events_collection = db.security_events

            # Check for duplicates
            existing = await events_collection.find_one({
                "event_id": enriched_event["event_id"]
            })
            if existing:
                processing_result["rejected"] = 1
                processing_result["errors"].append("Duplicate event")
                return processing_result

            await events_collection.insert_one(enriched_event)
            processing_result["stored"] = 1

            # Step 5: Correlate
            correlation_context = await self.correlation_engine.correlate_event(
                enriched_event,
                window_seconds=300
            )

            # Step 6: Detect
            detections = await self.detection_engine.evaluate_event(
                enriched_event,
                correlation_context
            )

            # Step 7: Generate Alerts
            for detection in detections:
                alert = await self.alert_service.generate_alert(
                    detection,
                    enriched_event,
                    correlation_context
                )
                processing_result["alerts_generated"] += 1

                # Step 8: Group into Incident
                if alert:
                    incident = await self.incident_service.group_alert_into_incident(alert)
                    if incident:
                        processing_result["incidents_created"] += 1

            processing_result["event_id"] = enriched_event["event_id"]
            processing_result["detections"] = len(detections)

            return processing_result

        except Exception as e:
            processing_result["rejected"] = 1
            processing_result["errors"].append(str(e))
            return processing_result

    async def ingest_bulk(
        self,
        raw_events: List[str],
        source_type: str,
        source_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ingest multiple raw events through the pipeline.

        Args:
            raw_events: List of raw log lines/strings
            source_type: The type of log source
            source_context: Additional context about the source

        Returns:
            Aggregate processing result
        """
        aggregate_result = {
            "ingestion_id": str(uuid.uuid4()),
            "source_type": source_type,
            "received": len(raw_events),
            "parsed": 0,
            "normalized": 0,
            "enriched": 0,
            "stored": 0,
            "rejected": 0,
            "alerts_generated": 0,
            "incidents_created": 0,
            "errors": [],
            "processing_time_ms": 0,
        }

        start_time = datetime.utcnow()

        for raw_event in raw_events:
            result = await self.ingest_event(raw_event, source_type, source_context)

            aggregate_result["parsed"] += result["parsed"]
            aggregate_result["normalized"] += result["normalized"]
            aggregate_result["enriched"] += result["enriched"]
            aggregate_result["stored"] += result["stored"]
            aggregate_result["rejected"] += result["rejected"]
            aggregate_result["alerts_generated"] += result["alerts_generated"]
            aggregate_result["incidents_created"] += result["incidents_created"]
            aggregate_result["errors"].extend(result["errors"])

        end_time = datetime.utcnow()
        aggregate_result["processing_time_ms"] = int(
            (end_time - start_time).total_seconds() * 1000
        )

        return aggregate_result

    async def ingest_file(
        self,
        file_content: str,
        source_type: str,
        source_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Ingest events from a file content string.

        Args:
            file_content: The file content as string
            source_type: The type of log source
            source_context: Additional context about the source

        Returns:
            Aggregate processing result
        """
        # Split file content into lines
        lines = file_content.strip().split('\n')
        # Filter empty lines
        lines = [line.strip() for line in lines if line.strip()]

        return await self.ingest_bulk(lines, source_type, source_context)
