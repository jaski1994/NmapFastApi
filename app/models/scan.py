from sqlalchemy import Column, String, JSON, DateTime
from app.core.database import Base

class DBScan(Base):
    __tablename__ = "scans"

    scan_id = Column(String, primary_key=True, index=True)
    target = Column(String, index=True)
    scan_type = Column(String)
    status = Column(String)
    start_time = Column(DateTime(timezone=True))
    summary = Column(JSON, nullable=True)
    results = Column(JSON, nullable=True)
