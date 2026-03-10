from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def get_scans():
    return {"message": "List of scans will be here"}

@router.post("/")
def run_scan():
    return {"message": "Scan started"}
