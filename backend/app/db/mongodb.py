from app.core.config import settings
from app.core.logging_config import get_logger
from motor.motor_asyncio import AsyncIOMotorClient

logger = get_logger("mongodb")


class MongoDB:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        """Connect to MongoDB."""
        logger.info("Connecting to MongoDB", url=settings.MONGODB_URL)
        self.client = AsyncIOMotorClient(settings.MONGODB_URL)
        self.db = self.client[settings.MONGODB_DB_NAME]
        logger.info("Connected to MongoDB")

    async def disconnect(self):
        """Disconnect from MongoDB."""
        if self.client:
            logger.info("Disconnecting from MongoDB")
            self.client.close()
            logger.info("Disconnected from MongoDB")

    async def check_connection(self) -> bool:
        """Check MongoDB connection."""
        try:
            await self.client.admin.command("ismaster")
            return True
        except Exception as e:
            logger.error("MongoDB connection error", error=str(e))
            return False


mongodb = MongoDB()
