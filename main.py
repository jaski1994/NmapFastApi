from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings
from app.core.database import Base, engine
from app.models.scan import DBScan # Import models to ensure they are registered

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": "Welcome to Nmap API"}
