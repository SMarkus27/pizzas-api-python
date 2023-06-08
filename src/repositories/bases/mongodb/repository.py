# Third-Party Library
from motor.motor_asyncio import AsyncIOMotorCollection

# Inner
from src.core.interfaces.repositories.bases.mongodb.interface import IBaseMongoDBRepo
from src.infrastructures.mongodb.infrastructure import MongoDBInfra


class BaseMongoDBRepo(MongoDBInfra, IBaseMongoDBRepo):
    _database: str = None
    _collection: str = None
    _collection_in_connection: AsyncIOMotorCollection = None

    @classmethod
    async def _set_base_connection(cls):
        if not (cls._collection and cls._database):
            raise Exception("What are you trying do it")

        client = cls.get_mongodb_client()
        database = client[cls._database]
        collection = database[cls._collection]
        return collection

    @classmethod
    async def get_base_collection(cls):
        if cls._collection_in_connection is None:
            cls._collection_in_connection: AsyncIOMotorCollection = await cls._set_base_connection()
        return cls._collection_in_connection

    @classmethod
    async def insert_one(cls, data: dict):
        collection = await cls.get_base_collection()
        await collection.insert_one(data)

    @classmethod
    async def find_all(cls, query: dict, projection: dict = None, limit: int = None, sort: tuple = None):
        collection = await cls.get_base_collection()
        result = collection.find(query, projection)
        if sort:
            result.sort(*sort)

        result.limit(limit)
        data = await result.to_list(limit)
        return data

    @classmethod
    async def find_one(cls, query: dict, projection: dict):
        collection = await cls.get_base_collection()
        result = await collection.find_one(query, projection)
        return result

    @classmethod
    async def update_one(cls, query: dict, new_data: dict, array_filters: list = None, upsert: bool = False):
        collection = await cls.get_base_collection()
        new = {"$set": new_data}
        result = await collection.update_one(query, new, array_filters=array_filters, upsert=upsert)
        return result

    @classmethod
    async def delete_one(cls, query: dict):
        collection = await cls.get_base_collection()
        result = await collection.delete_one(query)
        return result
