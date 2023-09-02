# Third-Party Library
from decouple import config

from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class PizzasRepository(BaseMongoDBRepo):
    _database: str = config("MONGODB_PIZZA_DATABASE")
    _collection: str = config("MONGODB_PIZZA_COLLECTION")
