from fastapi import APIRouter, BackgroundTasks, HTTPException, Path
import uuid
from datetime import datetime, timezone

from app.models.scan import ScanType, ScanStatus
from app.schemas.scan import ScanRequest, ScanResponse, ScanListResponse, ScanResult, ScanSummary
from app.schemas.store import get_scan, create_scan, list_scans
from app.services.nmap_scanner import run_nmap_scan
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=ScanResponse, status_code=202)
async def create_new_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = str(uuid.uuid4())
    start_time = datetime.now(timezone.utc)
    
    # Initialize in store
    scan_data = {
        "scan_id": scan_id,
        "target": request.target,
        "scan_type": request.scan_type.value,
        "status": ScanStatus.pending.value,
        "start_time": start_time,
        "summary": None,
        "results": None
    }
    create_scan(scan_id, scan_data)
    
    # Trigger background task
    logger.info("Scan requested", extra={"scan_id": scan_id, "target": request.target, "scan_type": request.scan_type.value})
    background_tasks.add_task(run_nmap_scan, scan_id, request.target, request.scan_type)
    
    return get_scan(scan_id)

@router.get("/{scan_id}", response_model=ScanResponse)
async def get_scan_status(scan_id: str = Path(..., title="The ID of the scan")):
    scan = get_scan(scan_id)
    if not scan:
        logger.warning("Scan status requested but not found", extra={"scan_id": scan_id})
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan

@router.get("/{scan_id}/results")
async def get_scan_results(scan_id: str = Path(..., title="The ID of the scan")):
    scan = get_scan(scan_id)
    if not scan:
        logger.warning("Scan results requested but not found", extra={"scan_id": scan_id})
        raise HTTPException(status_code=404, detail="Scan not found")
        
    if scan.status != ScanStatus.completed.value:
        logger.info("Scan results requested but not yet completed", extra={"scan_id": scan_id, "current_status": scan.status})
        raise HTTPException(status_code=400, detail=f"Scan results not available. Current status: {scan.status}")
        
    return scan.results

@router.get("/", response_model=list[ScanListResponse])
async def get_all_scans():
    scans = list_scans()
    # Sort scans by start_time descending (newest first)
    scans.sort(key=lambda x: x.start_time if x.start_time else datetime.min.replace(tzinfo=timezone.utc), reverse=True)
    return scans
