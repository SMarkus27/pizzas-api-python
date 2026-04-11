from motor.motor_asyncio import AsyncIOMotorDatabase

from src.core.settings import get_settings
from src.infrastructure.mongodb.repository import BaseMongoDBRepository


class OrderRepository(BaseMongoDBRepository):
    def __init__(self, database: AsyncIOMotorDatabase):
        settings = get_settings()
        collection_name = settings.MONGODB_ORDER_COLLECTION
        super().__init__(database, collection_name)
