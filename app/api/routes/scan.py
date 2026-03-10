from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.scan import DBScan, ScanType, ScanStatus
from app.services.nmap_scanner import run_nmap_scan
import uuid
from datetime import datetime, timezone

router = APIRouter()

@router.get("/")
def get_scans(db: Session = Depends(get_db)):
    return db.query(DBScan).all()

@router.post("/")
async def run_scan(target: str, scan_type: ScanType, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    scan_id = str(uuid.uuid4())
    new_scan = DBScan(
        scan_id=scan_id,
        target=target,
        scan_type=scan_type.value,
        status=ScanStatus.pending.value,
        start_time=datetime.now(timezone.utc)
    )
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)

    background_tasks.add_task(run_nmap_scan, scan_id, target, scan_type)
    
    return {"message": "Scan started", "scan_id": scan_id, "target": target}
