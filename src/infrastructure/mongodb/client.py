from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from src.infrastructure.settings import get_settings


class MongoDBConnection:
    _client: AsyncIOMotorClient = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            settings = get_settings()
            url = settings.MONGODB_CONNECTION_URL
            cls._client = AsyncIOMotorClient(url)
        return cls._client

    @classmethod
    def get_database(cls) -> AsyncIOMotorDatabase:
        client = cls.get_client()
        settings = get_settings()
        db_name = settings.MONGODB_DATABASE_NAME
        return client[db_name]

    @classmethod
    def close_client(cls):
        if cls._client is not None:
            cls._client.close()


async def get_db() -> AsyncIOMotorDatabase:
    return MongoDBConnection.get_database()
