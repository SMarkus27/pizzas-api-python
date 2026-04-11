from src.core.exceptions import NotFoundError
from src.repositories.pizzas.repository import PizzaRepository


class DeletePizzaService:
    def __init__(self, repository: PizzaRepository) -> None:
        self._repository = repository

    async def delete(self, pizza_external_id: str):
        query = {"external_id": pizza_external_id}

        result = await self._repository.find_one(query)

        if not result:
            raise NotFoundError()

        await self._repository.delete_one(query)
