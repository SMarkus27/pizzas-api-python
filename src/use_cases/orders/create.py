from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.order import Order
from src.domain.entities.store import Store
from src.domain.exceptions import NotFoundError
from src.domain.repositories.base import BaseRepositoryProtocol
from src.infrastructure.http.orders.schemas import CreateOrderInSchema


class CreateOrderUseCase:
    def __init__(
        self,
        order_repository: BaseRepositoryProtocol,
        store_repository: BaseRepositoryProtocol,
        pizza_repository: BaseRepositoryProtocol,
    ) -> None:
        self._order_repository = order_repository
        self._store_repository = store_repository
        self._pizza_repository = pizza_repository

    async def execute(self, data: CreateOrderInSchema) -> dict[str, str]:
        query = {"name": data.name}

        pizza_data = await self._pizza_repository.find_one(query, {"_id": False})
        if not pizza_data:
            raise NotFoundError("Pizza not found")

        store_data = await self._store_repository.find_one(query)
        if not store_data:
            raise NotFoundError(f"Store item '{data.name}' not found")

        store = Store(name=store_data["name"], quantity=store_data["quantity"])
        store.decrease_quantity(data.quantity)

        total_price = pizza_data["price"] * data.quantity
        Order(name=data.name, quantity=data.quantity, price=total_price)

        await self._store_repository.update_one(
            {"name": store.name},
            {"quantity": store.quantity, "updated_at": datetime.now(timezone.utc)},
        )

        external_id = str(uuid4())
        await self._order_repository.insert_one(
            {
                "external_id": external_id,
                "name": data.name,
                "quantity": data.quantity,
                "price": total_price,
                "created_at": datetime.now(timezone.utc),
                "updated_at": None,
            }
        )
        return {"order_external_id": external_id}
