from fastapi import APIRouter, Depends
from app.database.mongodb import MongoDB, get_database
from app.core.config import get_settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """Basic health check endpoint."""
    settings = get_settings()
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "0.1.0",
        "environment": settings.ENVIRONMENT
    }


@router.get("/ready")
async def readiness_check(db = Depends(get_database)):
    """Readiness check including database connectivity."""
    mongo_healthy = await MongoDB.health_check()
    
    return {
        "status": "ready" if mongo_healthy else "not_ready",
        "database": "connected" if mongo_healthy else "disconnected"
    }


@router.get("/live")
async def liveness_check():
    """Liveness check - service is running."""
    return {"status": "alive"}
