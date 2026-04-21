from datetime import datetime, timezone

from src.domain.entities.store import Store
from src.domain.exceptions import NotFoundError
from src.domain.repositories.base import BaseRepositoryProtocol
from src.infrastructure.http.stores.schemas import UpdateStoreInSchema


class UpdateStoreUseCase:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def _get_store_entity(self, name: str) -> Store:
        result = await self._repository.find_one({"name": name})
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
