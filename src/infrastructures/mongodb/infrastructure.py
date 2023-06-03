# Third-Party Library
from motor.motor_asyncio import AsyncIOMotorClient

# Inner
from src.core.interfaces.infrastructures.mongodb.interface import IMongoDBInfra


class MongoDBInfra(IMongoDBInfra):
    _mongodb_connection_url: str = "my_connecting_string"
    _mongodb_client: AsyncIOMotorClient = None

    @classmethod
    def get_mongodb_client(cls) -> AsyncIOMotorClient:
        if not cls._mongodb_connection_url:
            raise Exception("You forgot it something")

        if cls._mongodb_client is None:
            cls._mongo_client = AsyncIOMotorClient(cls._mongodb_connection_url)
        return cls._mongodb_client

