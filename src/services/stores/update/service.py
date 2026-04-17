from datetime import datetime, timezone

from src.core.exceptions import (
    NotFoundError,
)
from src.core.protocols.repository import BaseRepositoryProtocol
from src.domain.entities.store import Store
from src.services.stores.update.schemas import UpdateStoreInSchema


class UpdateStoreService:
    def __init__(self, repository: BaseRepositoryProtocol):
        self._repository = repository

    async def _get_store_entity(self, name: str) -> Store:
        query = {"name": name}
        result = await self._repository.find_one(query)

        if not result:
            raise NotFoundError(message=f"Store item '{name}' not found")

        return Store(name=result["name"], quantity=result["quantity"])

    async def increase(self, data: UpdateStoreInSchema) -> None:
        store = await self._get_store_entity(data.name)
        store.increase_quantity(data.quantity)

        await self._repository.update_one(
            {"name": store.name},
            {"quantity": store.quantity, "updated_at": datetime.now(timezone.utc)},
        )

    async def decrease(self, data: UpdateStoreInSchema) -> None:
        store = await self._get_store_entity(data.name)
        store.decrease_quantity(data.quantity)

        await self._repository.update_one(
            {"name": store.name},
            {"quantity": store.quantity, "updated_at": datetime.now(timezone.utc)},
        )
