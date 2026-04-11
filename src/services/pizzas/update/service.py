from datetime import datetime, timezone

from src.core.exceptions import  NotFoundException
from src.domain.models.pizza.update import UpdatePizzaInSchema
from src.repositories.pizzas.repository import PizzaRepository


class UpdatePizzaService:
    def __init__(self, repository: PizzaRepository) -> None:
        self._repository = repository


    async def update(self, pizza_external_id: str, data: UpdatePizzaInSchema) -> None:
        query = {"external_id": pizza_external_id}

        pizza = await self._repository.find_one(query)

        if not pizza:
            raise NotFoundException()

        new_data = data.model_dump(exclude_unset=True)
        new_data["updated_at"] = datetime.now(timezone.utc)

        await self._repository.update_one(query, new_data)

