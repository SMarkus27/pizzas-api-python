from src.core.utils import calculate_pages
from src.domain.repositories.base import BaseRepositoryProtocol


class ListStoresUseCase:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def get_all(self, page: int, size: int) -> dict:
        result, total_items = await self._repository.find_all_paginated(
            {}, page, size, {"_id": False}
        )
        total_pages = calculate_pages(total_items, size)

        return {
            "items": result,
            "total_items": total_items,
            "page": page,
            "total_pages": total_pages,
        }
