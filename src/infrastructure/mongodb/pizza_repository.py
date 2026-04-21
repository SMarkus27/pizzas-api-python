from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.repository import BaseMongoDBRepository
from src.infrastructure.settings import get_settings


class PizzaRepository(BaseMongoDBRepository):
    def __init__(self, database: AsyncIOMotorDatabase):
        settings = get_settings()
        super().__init__(database, settings.MONGODB_PIZZA_COLLECTION)
