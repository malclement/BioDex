from app.core.logging_config import get_logger
from app.db import pins as pins_service
from app.models.pin import Pin
from app.models.pin import PinCreate
from fastapi import APIRouter
from fastapi import HTTPException

router = APIRouter()
logger = get_logger("pins_api")


@router.post("/pins", response_model=Pin, status_code=201)
async def create_pin(pin: PinCreate):
    """
    Create a new pin.

    Args:
        pin: Pin data to save

    Returns:
        The created pin with a 201 Created status code
    """
    logger.info("Creating new pin", title=pin.title)

    try:
        created_pin = await pins_service.create_pin(pin)
        logger.info("Pin created successfully", pin_id=created_pin.id)
        return created_pin
    except Exception as e:
        logger.error("Error creating pin", error=str(e))
        raise HTTPException(status_code=500, detail="Error creating pin")
