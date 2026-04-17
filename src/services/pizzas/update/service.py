from datetime import datetime, timezone

from src.core.exceptions import NotFoundError
from src.core.protocols.repository import BaseRepositoryProtocol
from src.domain.entities.pizza import Pizza
from src.services.pizzas.update.schemas import UpdatePizzaInSchema


class UpdatePizzaService:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def update(self, pizza_external_id: str, data: UpdatePizzaInSchema) -> None:
        query = {"external_id": pizza_external_id}

        pizza_data = await self._repository.find_one(query)

        if not pizza_data:
            raise NotFoundError()

        updated_name = data.name if data.name is not None else pizza_data["name"]
        updated_price = data.price if data.price is not None else pizza_data["price"]
        updated_ingredients = (
            data.ingredients
            if data.ingredients is not None
            else pizza_data["ingredients"]
        )

        Pizza(name=updated_name, price=updated_price, ingredients=updated_ingredients)

        new_data = data.model_dump(exclude_unset=True)
        new_data["updated_at"] = datetime.now(timezone.utc)

        await self._repository.update_one(query, new_data)
