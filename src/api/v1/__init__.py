"""API v1 routes"""

from fastapi import APIRouter
from src.api.v1.routes import trends, agents, health

router = APIRouter(prefix="/v1", tags=["v1"])

# Include route modules
router.include_router(trends.router, prefix="/trends", tags=["trends"])
router.include_router(agents.router, prefix="/agents", tags=["agents"])
router.include_router(health.router, tags=["health"])
