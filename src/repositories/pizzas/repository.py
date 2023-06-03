from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class PizzasRepository(BaseMongoDBRepo):
    _database: str = ""
    _collection: str = ""
