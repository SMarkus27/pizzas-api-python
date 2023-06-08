from src.repositories.bases.mongodb.repository import BaseMongoDBRepo


class PizzasRepository(BaseMongoDBRepo):
    _database: str = "teste"
    _collection: str = "teste"
