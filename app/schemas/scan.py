import re
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.scan import ScanType, ScanStatus

# Regex for IPv4 or Hostname
TARGET_REGEX = r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$|^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}$|^localhost$"

class ScanRequest(BaseModel):
    target: str = Field(..., description="Target IP or hostname")
    scan_type: ScanType

    @field_validator("target")
    @classmethod
    def validate_target(cls, v: str) -> str:
        if not re.match(TARGET_REGEX, v):
            raise ValueError("Target must be a valid IP address or hostname")
        return v

class ScanSummary(BaseModel):
    open_ports_count: int
    duration_seconds: float

class PortResult(BaseModel):
    port: int
    protocol: str
    state: str
    service: Optional[str] = None

class ScanResult(BaseModel):
    host: str
    command: str
    ports: List[PortResult]
    start_time: str
    end_time: str

class ScanListResponse(BaseModel):
    scan_id: str
    target: str
    scan_type: ScanType
    status: ScanStatus
    start_time: datetime

    model_config = ConfigDict(from_attributes=True)

class ScanResponse(ScanListResponse):
    summary: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)
