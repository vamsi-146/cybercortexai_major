from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import get_settings
from app.database.mongodb import MongoDB
from app.api.routes import auth, health, users, events, alerts, incidents, assets, datasources, dashboard, ingestion
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

settings = get_settings()

# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="AI-driven Security Operations Center (SOC) Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)


# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Handle application startup."""
    logger.info("Starting CyberCortex API...")
    await MongoDB.connect()
    logger.info("MongoDB connected successfully")


@app.on_event("shutdown")
async def shutdown_event():
    """Handle application shutdown."""
    logger.info("Shutting down CyberCortex API...")
    await MongoDB.close()
    logger.info("MongoDB connection closed")


# Include routers
app.include_router(health.router, prefix=settings.API_V1_PREFIX)
app.include_router(auth.router, prefix=settings.API_V1_PREFIX)
app.include_router(users.router, prefix=settings.API_V1_PREFIX)
app.include_router(events.router, prefix=settings.API_V1_PREFIX)
app.include_router(alerts.router, prefix=settings.API_V1_PREFIX)
app.include_router(incidents.router, prefix=settings.API_V1_PREFIX)
app.include_router(assets.router, prefix=settings.API_V1_PREFIX)
app.include_router(datasources.router, prefix=settings.API_V1_PREFIX)
app.include_router(dashboard.router, prefix=settings.API_V1_PREFIX)
app.include_router(ingestion.router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )
