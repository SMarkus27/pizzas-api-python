from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class OrderRepository(BaseMongoDBRepo):
    _database: str = ""
    _collection: str = ""
