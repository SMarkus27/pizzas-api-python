from datetime import datetime, timezone
from uuid import uuid4

from src.core.exceptions import ConflictError
from src.core.protocols.repository import BaseRepositoryProtocol
from src.domain.entities.pizza import Pizza
from src.services.pizzas.create.schemas import CreatePizzaInSchema


class CreatePizzaService:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def create(self, data: CreatePizzaInSchema):
        pizza = Pizza(name=data.name, price=data.price, ingredients=data.ingredients)

        query = {"name": pizza.name}
        existing_pizza = await self._repository.find_one(query)
        if existing_pizza:
            raise ConflictError("Pizza already exists! Try another name.")

        external_id = str(uuid4())
        pizza_to_save = {
            "external_id": external_id,
            "name": pizza.name,
            "price": pizza.price,
            "ingredients": pizza.ingredients,
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
        }

        await self._repository.insert_one(pizza_to_save)
        return {"pizza_external_id": external_id}
