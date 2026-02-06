"""FastAPI application and API routes"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging
import os

from src.config.settings import settings
from src.config.security import get_security_settings, secrets_manager

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("Starting Project Chimera API...")
    
    # Validate secrets
    validation = secrets_manager.validate_secrets()
    if validation["warnings"]:
        for warning in validation["warnings"]:
            logger.warning(f"Security warning: {warning}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Project Chimera API...")


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    app = FastAPI(
        title="Project Chimera API",
        description="Autonomous AI Influencer Factory - API",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan
    )
    
    # Security settings
    security_settings = get_security_settings()
    
    # CORS middleware
    if security_settings.enable_cors:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=security_settings.allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Security headers middleware
    if security_settings.enable_security_headers:
        @app.middleware("http")
        async def add_security_headers(request, call_next):
            response = await call_next(request)
            response.headers["X-Content-Type-Options"] = "nosniff"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-XSS-Protection"] = "1; mode=block"
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            return response
    
    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request, exc):
        logger.error(f"Unhandled exception: {exc}", exc_info=True)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal server error"}
        )
    
    # Include routers
    from src.api.v1 import router as v1_router
    app.include_router(v1_router, prefix="/api/v1")
    
    # Health check endpoint
    @app.get("/health")
    async def health_check():
        """Health check endpoint"""
        return {
            "status": "healthy",
            "version": "0.1.0",
            "environment": os.getenv("ENVIRONMENT", "development")
        }
    
    return app


# Create app instance
app = create_app()
