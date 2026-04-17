from datetime import datetime, timezone
from uuid import uuid4

from src.core.exceptions import NotFoundError
from src.core.protocols.repository import BaseRepositoryProtocol
from src.domain.entities.order import Order
from src.domain.entities.store import Store
from src.services.orders.create.schemas import CreateOrderInSchema


class CreateOrderService:
    def __init__(
        self,
        order_repo: BaseRepositoryProtocol,
        store_repo: BaseRepositoryProtocol,
        pizza_repo: BaseRepositoryProtocol,
    ):
        self.order_repo = order_repo
        self.store_repo = store_repo
        self.pizza_repo = pizza_repo

    async def create(self, data: CreateOrderInSchema):
        query = {"name": data.name}

        pizza_data = await self.pizza_repo.find_one(query, {"_id": False})
        if not pizza_data:
            raise NotFoundError("Pizza not found")

        store_data = await self.store_repo.find_one(query)
        if not store_data:
            raise NotFoundError(f"Store item '{data.name}' not found")

        store = Store(name=store_data["name"], quantity=store_data["quantity"])
        store.decrease_quantity(data.quantity)

        pizza_price = pizza_data.get("price")
        total_price = pizza_price * data.quantity
        Order(name=data.name, quantity=data.quantity, price=total_price)

        await self.store_repo.update_one(
            {"name": store.name},
            {"quantity": store.quantity, "updated_at": datetime.now(timezone.utc)},
        )

        external_id = str(uuid4())
        order_to_save = {
            "external_id": external_id,
            "name": data.name,
            "quantity": data.quantity,
            "price": total_price,
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
        }
        await self.order_repo.insert_one(order_to_save)

        return {"order_external_id": external_id}
