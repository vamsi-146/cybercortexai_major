from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class ResourceType(str, Enum):
    USER = "USER"
    ALERT = "ALERT"
    INCIDENT = "INCIDENT"
    INVESTIGATION = "INVESTIGATION"
    RULE = "RULE"
    SETTING = "SETTING"
    DATA_SOURCE = "DATA_SOURCE"


class AuditAction(str, Enum):
    LOGIN = "LOGIN"
    LOGOUT = "LOGOUT"
    CREATE = "CREATE"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    STATUS_CHANGE = "STATUS_CHANGE"
    ASSIGNMENT = "ASSIGNMENT"


class AuditLogCreate(BaseModel):
    user_id: Optional[str] = None
    username: str
    action: AuditAction
    resource_type: ResourceType
    resource_id: str
    changes: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    result: str = "SUCCESS"  # SUCCESS, FAILURE


class AuditLog(BaseModel):
    id: str
    timestamp: datetime
    user_id: Optional[str] = None
    username: str
    action: AuditAction
    resource_type: ResourceType
    resource_id: str
    changes: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    result: str
    session_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
