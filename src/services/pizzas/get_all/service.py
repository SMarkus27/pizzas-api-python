from src.core.protocols.repository import BaseRepositoryProtocol
from src.core.utils import calculate_pages


class GetAllPizzaService:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def get_all(self, page: int, size: int):
        projection = {"_id": 0}

        result, total_items = await self._repository.find_all_paginated(
            {}, page, size, projection=projection
        )

        total_pages = calculate_pages(total_items, size)

        return {
            "items": result,
            "total_items": total_items,
            "page": page,
            "total_pages": total_pages,
        }
