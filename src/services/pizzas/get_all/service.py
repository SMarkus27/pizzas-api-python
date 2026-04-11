from src.repositories.pizzas.repository import PizzaRepository


class GetAllPizzaService:
    def __init__(self, repository: PizzaRepository) -> None:
        self._repository = repository


    async def get_all(self, page: int, size: int):
        projection = {"_id": 0}

        result, total_items = await self._repository.find_all_paginated({}, page, size, projection=projection)

        total_pages = self._repository.calculate_pages(total_items, size)

        result = {
            "result": result,
            "total_items": total_items,
            "page": page,
            "total_pages": total_pages
        }

        return result
