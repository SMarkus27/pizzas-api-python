from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.store import Store
from src.domain.exceptions import ConflictError
from src.domain.repositories.base import BaseRepositoryProtocol
from src.infrastructure.http.stores.schemas import CreateStoreInSchema


class CreateStoreUseCase:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def execute(self, data: CreateStoreInSchema) -> dict[str, str]:
        store = Store(name=data.name, quantity=data.quantity)

        existing_item = await self._repository.find_one({"name": store.name})
        if existing_item:
            raise ConflictError(message="Store item already exists")

        external_id = str(uuid4())
        await self._repository.insert_one(
            {
                "external_id": external_id,
                "name": store.name,
                "quantity": store.quantity,
                "created_at": datetime.now(timezone.utc),
                "updated_at": None,
            }
        )
        return {"store_external_id": external_id}
