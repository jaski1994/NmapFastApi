from typing import Dict, Any, List
from app.core.database import SessionLocal
from app.models.scan import DBScan

def get_scan(scan_id: str) -> DBScan:
    db = SessionLocal()
    try:
        return db.query(DBScan).filter(DBScan.scan_id == scan_id).first()
    finally:
        db.close()

def create_scan(scan_id: str, scan_data: Dict[str, Any]):
    db = SessionLocal()
    try:
        new_scan = DBScan(**scan_data)
        db.add(new_scan)
        db.commit()
    finally:
        db.close()

def list_scans() -> List[DBScan]:
    db = SessionLocal()
    try:
        return db.query(DBScan).all()
    finally:
        db.close()

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
