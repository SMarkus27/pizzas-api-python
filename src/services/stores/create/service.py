from src.core.exceptions import ConflictError
from src.domain.models.store.model import CreateStoreInSchema
from src.infrastructure.documents.store import StoreDocument
from src.repositories.store.repository import StoreRepository


class CreateStoreService:
    def __init__(self, repository: StoreRepository):
        self._repository = repository

    async def create(self, data: CreateStoreInSchema):
        query = {"name": data.name}

        result = await self._repository.find_one(query)

        if result:
            raise ConflictError(message="Store item already exist")

        store = StoreDocument(name=data.name, quantity=data.quantity)

        await self._repository.insert_one(store.to_dict())
        return {"store_external_id": store.external_id}
