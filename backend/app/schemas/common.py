from pydantic import BaseModel, Field
from typing import Optional, List, Generic, TypeVar
from enum import Enum


class Severity(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class IncidentStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    CONTAINED = "CONTAINED"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"


class AlertStatus(str, Enum):
    NEW = "NEW"
    TRIAGED = "TRIAGED"
    INVESTIGATING = "INVESTIGATING"
    RESOLVED = "RESOLVED"
    FALSE_POSITIVE = "FALSE_POSITIVE"
    CLOSED = "CLOSED"


class AssetType(str, Enum):
    WORKSTATION = "WORKSTATION"
    SERVER = "SERVER"
    DOMAIN_CONTROLLER = "DOMAIN_CONTROLLER"
    NETWORK_DEVICE = "NETWORK_DEVICE"
    CLOUD_RESOURCE = "CLOUD_RESOURCE"
    APPLICATION = "APPLICATION"
    DATABASE = "DATABASE"
    UNKNOWN = "UNKNOWN"


class SourceType(str, Enum):
    WINDOWS = "WINDOWS"
    LINUX = "LINUX"
    FIREWALL = "FIREWALL"
    IDS = "IDS"
    EDR = "EDR"
    VPN = "VPN"
    PROXY = "PROXY"
    IDENTITY = "IDENTITY"
    CLOUD = "CLOUD"
    APPLICATION = "APPLICATION"
    CUSTOM = "CUSTOM"


class Criticality(str, Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class PaginatedResponse(BaseModel, Generic[TypeVar]):
    items: List[TypeVar]
    page: int
    page_size: int
    total: int
    pages: int


class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[dict] = None


class SuccessResponse(BaseModel):
    success: bool = True
    message: str
