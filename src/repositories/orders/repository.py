# Third-Party Library
from decouple import config

from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class OrderRepository(BaseMongoDBRepo):
    _database: str = config("MONGODB_ORDER_DATABASE")
    _collection: str = config("MONGODB_ORDER_COLLECTION")
