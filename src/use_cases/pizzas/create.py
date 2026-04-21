from datetime import datetime, timezone
from uuid import uuid4

from src.domain.entities.pizza import Pizza
from src.domain.exceptions import ConflictError
from src.domain.repositories.base import BaseRepositoryProtocol
from src.infrastructure.http.pizzas.schemas import CreatePizzaInSchema


class CreatePizzaUseCase:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def execute(self, data: CreatePizzaInSchema) -> dict[str, str]:
        pizza = Pizza(name=data.name, price=data.price, ingredients=data.ingredients)

        existing_pizza = await self._repository.find_one({"name": pizza.name})
        if existing_pizza:
            raise ConflictError("Pizza already exists! Try another name.")

        external_id = str(uuid4())
        await self._repository.insert_one(
            {
                "external_id": external_id,
                "name": pizza.name,
                "price": pizza.price,
                "ingredients": pizza.ingredients,
                "created_at": datetime.now(timezone.utc),
                "updated_at": None,
            }
        )
        return {"pizza_external_id": external_id}
