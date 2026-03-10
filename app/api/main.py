from fastapi import APIRouter

from app.api.routes import scan

api_router = APIRouter()
api_router.include_router(scan.router, prefix="/scans", tags=["scans"])
