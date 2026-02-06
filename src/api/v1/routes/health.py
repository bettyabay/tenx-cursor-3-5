"""Health check endpoints"""

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import text, create_engine
from src.config.settings import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    timestamp: datetime
    version: str
    services: dict


async def check_database():
    """Check database connectivity"""
    try:
        from sqlalchemy import create_engine
        engine = create_engine(settings.database_url)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "message": "Database connection OK"}
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {"status": "unhealthy", "message": str(e)}


@router.get("/", response_model=HealthResponse)
async def health_check():
    """
    Comprehensive health check endpoint.
    
    Returns:
        Health status of the API and all services
    """
    db_status = await check_database()
    
    return HealthResponse(
        status="healthy" if db_status["status"] == "healthy" else "degraded",
        timestamp=datetime.utcnow(),
        version="0.1.0",
        services={
            "database": db_status,
            "api": {"status": "healthy"}
        }
    )


@router.get("/ready")
async def readiness_check():
    """
    Readiness check for Kubernetes/Docker health probes.
    
    Returns:
        200 if ready, 503 if not ready
    """
    db_status = await check_database()
    
    if db_status["status"] != "healthy":
        from fastapi import status
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"status": "not_ready", "reason": "Database unavailable"}
        )
    
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """
    Liveness check for Kubernetes/Docker health probes.
    
    Returns:
        Always 200 if API is running
    """
    return {"status": "alive"}
