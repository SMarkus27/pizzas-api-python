# Third-Party Library
from decouple import config

from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class StoreRepository(BaseMongoDBRepo):
    _database: str = config("MONGODB_STORE_DATABASE")
    _collection: str = config("MONGODB_STORE_COLLECTION")
