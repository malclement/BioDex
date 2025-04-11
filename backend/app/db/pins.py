from datetime import datetime

from app.core.logging_config import get_logger
from app.db.mongodb import mongodb
from app.models.pin import PinCreate
from app.models.pin import PinInDB

logger = get_logger("pins_db")


async def create_pin(pin: PinCreate) -> PinInDB:
    """
    Create a new pin in the database.

    Args:
        pin: The pin data to create

    Returns:
        The created pin
    """
    pin_data = pin.model_dump()
    pin_data["created_at"] = datetime.utcnow()
    pin_data["updated_at"] = datetime.utcnow()

    result = await mongodb.db.pins.insert_one(pin_data)

    # Get the created pin
    created_pin = await mongodb.db.pins.find_one({"_id": result.inserted_id})

    logger.info("Pin created in database", pin_id=str(result.inserted_id))

    return PinInDB.from_mongo(created_pin)


async def create_indexes():
    """Create necessary indexes for the pins collection."""
    # Create geospatial index for location queries
    await mongodb.db.pins.create_index([("lat", 1), ("lng", 1)])
    # Create text index for title and description searches
    await mongodb.db.pins.create_index([("title", "text"), ("description", "text")])

    logger.info("Created indexes for pins collection")
