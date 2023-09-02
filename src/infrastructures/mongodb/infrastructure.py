# Third-Party Libraries
from motor.motor_asyncio import AsyncIOMotorClient
from decouple import config

# Inner
from src.core.interfaces.infrastructures.mongodb.interface import IMongoDBInfra


class MongoDBInfra(IMongoDBInfra):
    _mongodb_connection_url: str = config("MONGODB_CONNECTION_URL")
    _mongodb_client: AsyncIOMotorClient = None

    @classmethod
    def get_mongodb_client(cls) -> AsyncIOMotorClient:
        if not cls._mongodb_connection_url:
            raise Exception("You forgot it something")

        if cls._mongodb_client is None:
            cls._mongodb_client = AsyncIOMotorClient(cls._mongodb_connection_url)
        return cls._mongodb_client
