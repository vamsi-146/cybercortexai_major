from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from .common import SourceType


class DataSourceCreate(BaseModel):
    source_id: str = Field(..., min_length=1)
    name: str
    type: SourceType
    description: Optional[str] = None
    enabled: bool = True
    configuration_metadata: Optional[Dict[str, Any]] = {}


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None
    configuration_metadata: Optional[Dict[str, Any]] = None


class DataSource(BaseModel):
    id: str
    source_id: str
    name: str
    type: SourceType
    description: Optional[str] = None
    status: str = "ENABLED"
    enabled: bool = True
    last_event_at: Optional[datetime] = None
    event_count: int = 0
    configuration_metadata: Dict[str, Any] = {}
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class DataSourceFilter(BaseModel):
    type: Optional[SourceType] = None
    enabled: Optional[bool] = None
    status: Optional[str] = None
