from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class StoreRepository(BaseMongoDBRepo):
    _database: str = ""
    _collection: str = ""

    