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
    now = datetime.utcnow()
    pin_data["created_at"] = now
    pin_data["updated_at"] = now

    result = await mongodb.db.pins.insert_one(pin_data)

    pin_data["_id"] = result.inserted_id

    logger.info("Pin created in database", pin_id=str(result.inserted_id))

    return PinInDB.from_mongo(pin_data)


async def create_indexes():
    """Create necessary indexes for the pins collection."""
    # Create geospatial index for location queries
    await mongodb.db.pins.create_index([("lat", 1), ("lng", 1)])
    # Create text index for title and description searches
    await mongodb.db.pins.create_index([("title", "text"), ("description", "text")])

    logger.info("Created indexes for pins collection")
