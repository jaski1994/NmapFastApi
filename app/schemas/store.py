from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.scan import DBScan

def get_scan(db: Session, scan_id: str) -> DBScan:
    return db.query(DBScan).filter(DBScan.scan_id == scan_id).first()

def create_scan(db: Session, scan_id: str, scan_data: Dict[str, Any]):
    new_scan = DBScan(**scan_data)
    db.add(new_scan)
    db.commit()
    db.refresh(new_scan)
    return new_scan

def list_scans(db: Session) -> List[DBScan]:
    return db.query(DBScan).all()

def update_scan(db: Session, scan_id: str, update_data: Dict[str, Any]):
    scan = db.query(DBScan).filter(DBScan.scan_id == scan_id).first()
    if scan:
        for key, value in update_data.items():
            setattr(scan, key, value)
        db.commit()
        db.refresh(scan)
        return scan
    return None
