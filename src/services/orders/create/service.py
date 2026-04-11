from src.core.exceptions import BadRequestError, NotFoundError
from src.domain.models.order.model import CreateOrderInSchema
from src.infrastructure.documents.order import OrderDocument
from src.repositories.orders.repository import OrderRepository
from src.repositories.pizzas.repository import PizzaRepository
from src.repositories.store.repository import StoreRepository
from src.services.stores.update.service import UpdateStoreService


class CreateOrderService:
    def __init__(
        self,
        order_repo: OrderRepository,
        store_repo: StoreRepository,
        pizza_repo: PizzaRepository,
        update_store_service: UpdateStoreService,
    ):
        self.order_repo = order_repo
        self.store_repo = store_repo
        self.pizza_repo = pizza_repo
        self.update_store_service = update_store_service

    async def create(self, data: CreateOrderInSchema):
        query = {"name": data.name}

        result = await self.store_repo.find_one(query, {"_id": False})

        if not result:
            raise NotFoundError()

        store_quantity = result.get("quantity")

        if store_quantity == 0:
            raise BadRequestError("Item is empty")

        if store_quantity < data.quantity:
            raise BadRequestError(f"Quantity must be greater than {store_quantity}")

        await self.update_store_service.update(data)

        pizza_data = await self.pizza_repo.find_one(query, {"_id": False})

        if not pizza_data:
            raise NotFoundError("Pizza not found")

        pizza_price = pizza_data.get("price")

        order = OrderDocument(
            name=data.name, quantity=data.quantity, price=pizza_price * data.quantity
        )

        await self.order_repo.insert_one(order.to_dict())

        return {"order_external_id": order.external_id}
