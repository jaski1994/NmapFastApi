from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from app.models.scan import ScanType, ScanStatus

class ScanRequest(BaseModel):
    target: str
    scan_type: ScanType

class ScanSummary(BaseModel):
    pass # Add fields if needed later

class PortResult(BaseModel):
    port_id: int
    state: str
    service: Optional[str] = None

class ScanResult(BaseModel):
    host: str
    ports: List[PortResult]
    start_time: str
    end_time: str

class ScanListResponse(BaseModel):
    scan_id: str
    target: str
    scan_type: ScanType
    status: ScanStatus
    start_time: datetime

    class Config:
        from_attributes = True

class ScanResponse(ScanListResponse):
    summary: Optional[Dict[str, Any]] = None
    results: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
