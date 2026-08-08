"""Ingestion API routes for log upload and processing."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
from app.api.dependencies.auth import get_current_user
from app.ingestion.services import IngestionService
from app.schemas.user import UserResponse


router = APIRouter(prefix="/ingestion", tags=["ingestion"])
ingestion_service = IngestionService()


@router.post("/event")
async def ingest_single_event(
    raw_event: str,
    source_type: str = Form(...),
    source_name: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Ingest a single security event.

    Args:
        raw_event: The raw log line/string
        source_type: The type of log source (windows, linux, firewall, json)
        source_name: Optional name for the data source

    Returns:
        Processing result
    """
    # Check authorization
    if current_user.role not in ["ADMIN", "SOC_ANALYST", "SECURITY_ENGINEER"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    source_context = {
        "source_name": source_name or f"{source_type}_upload",
        "uploaded_by": current_user.username,
    }

    result = await ingestion_service.ingest_event(raw_event, source_type, source_context)
    return result


@router.post("/bulk")
async def ingest_bulk_events(
    raw_events: list[str],
    source_type: str = Form(...),
    source_name: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Ingest multiple security events.

    Args:
        raw_events: List of raw log lines/strings
        source_type: The type of log source
        source_name: Optional name for the data source

    Returns:
        Aggregate processing result
    """
    # Check authorization
    if current_user.role not in ["ADMIN", "SOC_ANALYST", "SECURITY_ENGINEER"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    source_context = {
        "source_name": source_name or f"{source_type}_bulk_upload",
        "uploaded_by": current_user.username,
    }

    result = await ingestion_service.ingest_bulk(raw_events, source_type, source_context)
    return result


@router.post("/upload")
async def upload_log_file(
    file: UploadFile = File(...),
    source_type: str = Form(...),
    source_name: Optional[str] = Form(None),
    current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Upload and ingest a log file.

    Args:
        file: The log file to upload
        source_type: The type of log source
        source_name: Optional name for the data source

    Returns:
        Aggregate processing result
    """
    # Check authorization
    if current_user.role not in ["ADMIN", "SOC_ANALYST", "SECURITY_ENGINEER"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # Validate file type
    allowed_extensions = {".log", ".txt", ".json", ".jsonl"}
    file_ext = None
    for ext in allowed_extensions:
        if file.filename.lower().endswith(ext):
            file_ext = ext
            break

    if not file_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(allowed_extensions)}"
        )

    # Validate file size (max 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File too large. Maximum size: 10MB")

    file_content = content.decode('utf-8', errors='ignore')

    source_context = {
        "source_name": source_name or file.filename,
        "uploaded_by": current_user.username,
        "file_name": file.filename,
    }

    result = await ingestion_service.ingest_file(file_content, source_type, source_context)
    return result


@router.get("/status/{ingestion_id}")
async def get_ingestion_status(
    ingestion_id: str,
    current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get the status of a bulk ingestion operation.

    Note: In this implementation, ingestion is synchronous, so this
    endpoint returns the result if it was stored. For async ingestion,
    this would check the status of a background job.

    Args:
        ingestion_id: The ingestion ID

    Returns:
        Ingestion status/result
    """
    # Check authorization
    if current_user.role not in ["ADMIN", "SOC_ANALYST", "SECURITY_ENGINEER", "VIEWER"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    # For synchronous ingestion, we don't store results
    # This is a placeholder for future async implementation
    return {
        "ingestion_id": ingestion_id,
        "status": "completed",
        "message": "Ingestion completed synchronously",
    }


@router.get("/stats")
async def get_ingestion_statistics(
    current_user: UserResponse = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get ingestion statistics.

    Args:
        None

    Returns:
        Ingestion statistics
    """
    # Check authorization
    if current_user.role not in ["ADMIN", "SOC_ANALYST", "SECURITY_ENGINEER", "VIEWER"]:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    from app.database.mongodb import get_database

    db = await get_database()
    events_collection = db.security_events
    alerts_collection = db.alerts
    incidents_collection = db.incidents

    # Get counts
    total_events = await events_collection.count_documents({})
    total_alerts = await alerts_collection.count_documents({})
    total_incidents = await incidents_collection.count_documents({})

    # Get counts by source type
    events_by_source = {}
    for source_type in ["windows", "linux", "firewall", "json"]:
        count = await events_collection.count_documents({"source_type": source_type})
        events_by_source[source_type] = count

    return {
        "total_events": total_events,
        "total_alerts": total_alerts,
        "total_incidents": total_incidents,
        "events_by_source": events_by_source,
    }
