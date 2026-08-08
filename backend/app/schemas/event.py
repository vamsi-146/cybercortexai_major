from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from .common import Severity, SourceType


class NormalizedEvent(BaseModel):
    timestamp: datetime
    event_type: str
    category: Optional[str] = None
    severity: Optional[Severity] = None
    source_ip: Optional[str] = None
    destination_ip: Optional[str] = None
    source_port: Optional[int] = None
    destination_port: Optional[int] = None
    protocol: Optional[str] = None
    user: Optional[str] = None
    host: Optional[str] = None
    process: Optional[str] = None
    file_hash: Optional[str] = None
    url: Optional[str] = None
    domain: Optional[str] = None
    description: Optional[str] = None


class SecurityEventCreate(BaseModel):
    event_id: str = Field(..., min_length=1)
    source: str
    source_type: SourceType
    raw_event: Dict[str, Any]
    normalized_event: NormalizedEvent
    received_at: Optional[datetime] = None


class SecurityEvent(BaseModel):
    id: str
    event_id: str
    source: str
    source_type: SourceType
    raw_event: Dict[str, Any]
    normalized_event: NormalizedEvent
    received_at: datetime
    created_at: datetime
    processed: bool = False
    alert_id: Optional[str] = None

    class Config:
        from_attributes = True


class EventFilter(BaseModel):
    source_type: Optional[SourceType] = None
    severity: Optional[Severity] = None
    event_type: Optional[str] = None
    src_ip: Optional[str] = None
    dst_ip: Optional[str] = None
    username: Optional[str] = None
    hostname: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
