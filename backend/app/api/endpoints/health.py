from typing import Any
from typing import Dict

from app.core.config import settings
from app.core.logging_config import get_logger
from app.db.mongodb import mongodb
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()
logger = get_logger("health")


async def get_db_status():
    """Get database connection status."""
    connected = await mongodb.check_connection()
    return {"connected": connected}


@router.get("/health", response_model=Dict[str, Any])
async def health_check(db_status: Dict = Depends(get_db_status)):
    """
    Health check endpoint.

    Returns:
        dict: Health status of the API and its dependencies
    """
    logger.info("Health check requested")

    health_data = {
        "status": "healthy",
        "version": settings.API_VERSION,
        "environment": settings.ENVIRONMENT,
        "mongodb": db_status,
    }

    if not db_status["connected"]:
        health_data["status"] = "unhealthy"

    return health_data
