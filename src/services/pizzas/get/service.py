from src.core.exceptions import NotFoundException
from src.repositories.pizzas.repository import PizzaRepository


class GetPizzaService:
    def __init__(self, repository: PizzaRepository) -> None:
        self._repository = repository


    async def get_one(self, pizza_external_id: str):
        query = {"external_id": pizza_external_id}
        projection = {"_id": 0}

        result = await self._repository.find_one(query, projection)
        if not result:
            raise NotFoundException()

        return result


