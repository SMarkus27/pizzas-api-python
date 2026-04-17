from datetime import datetime, timezone
from uuid import uuid4

from src.core.exceptions import ConflictError
from src.core.protocols.repository import BaseRepositoryProtocol
from src.domain.entities.store import Store
from src.services.stores.create.schemas import CreateStoreInSchema


class CreateStoreService:
    def __init__(self, repository: BaseRepositoryProtocol):
        self._repository = repository

    async def create(self, data: CreateStoreInSchema):
        store = Store(name=data.name, quantity=data.quantity)

        query = {"name": store.name}
        existing_item = await self._repository.find_one(query)
        if existing_item:
            raise ConflictError(message="Store item already exists")

        external_id = str(uuid4())
        store_to_save = {
            "external_id": external_id,
            "name": store.name,
            "quantity": store.quantity,
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
        }

        await self._repository.insert_one(store_to_save)
        return {"store_external_id": external_id}
