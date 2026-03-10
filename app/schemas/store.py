from typing import Dict, Any
from app.core.database import SessionLocal
from app.models.scan import DBScan

def update_scan(scan_id: str, update_data: Dict[str, Any]):
    db = SessionLocal()
    try:
        scan = db.query(DBScan).filter(DBScan.scan_id == scan_id).first()
        if scan:
            for key, value in update_data.items():
                setattr(scan, key, value)
            db.commit()
    finally:
        db.close()
