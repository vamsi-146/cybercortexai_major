from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .common import AssetType, Criticality


class AssetCreate(BaseModel):
    asset_id: str = Field(..., min_length=1)
    hostname: str
    ip_addresses: List[str] = []
    mac_addresses: Optional[List[str]] = []
    asset_type: AssetType
    operating_system: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    criticality: Criticality


class AssetUpdate(BaseModel):
    hostname: Optional[str] = None
    ip_addresses: Optional[List[str]] = None
    mac_addresses: Optional[List[str]] = None
    asset_type: Optional[AssetType] = None
    operating_system: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    criticality: Optional[Criticality] = None
    risk_score: Optional[int] = Field(None, ge=0, le=100)
    status: Optional[str] = None


class Asset(BaseModel):
    id: str
    asset_id: str
    hostname: str
    ip_addresses: List[str] = []
    mac_addresses: Optional[List[str]] = []
    asset_type: AssetType
    operating_system: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
    criticality: Criticality
    risk_score: int = Field(default=0, ge=0, le=100)
    vulnerabilities: List[str] = []
    first_seen: datetime
    last_seen: datetime
    status: str = "ACTIVE"
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AssetFilter(BaseModel):
    asset_type: Optional[AssetType] = None
    criticality: Optional[Criticality] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    department: Optional[str] = None
