from datetime import datetime, timezone

from src.core.exceptions import (
    BadRequestError,
    ConflictError,
    NotFoundError,
)
from src.domain.models.store.model import UpdateStoreInSchema
from src.repositories.store.repository import StoreRepository


class UpdateStoreService:
    def __init__(self, repository: StoreRepository):
        self._repository = repository

    async def update(self, data: UpdateStoreInSchema) -> None:
        query = {"name": data.name}

        result = await self._repository.find_one(query)

        if not result:
            raise NotFoundError()

        old_quantity = result.get("quantity")
        if old_quantity == 0:
            raise ConflictError("This product is empty")

        quantity = data.quantity

        if quantity > old_quantity:
            raise BadRequestError(f"Quantity must be less than {old_quantity}")

        new_quantity = old_quantity - quantity

        await self._repository.update_one(
            query, {"quantity": new_quantity, "updated_at": datetime.now(timezone.utc)}
        )
