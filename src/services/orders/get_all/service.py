from src.core.protocols.repository import BaseRepositoryProtocol
from src.core.utils import calculate_pages


class GetAllOrderService:
    def __init__(self, repository: BaseRepositoryProtocol):
        self._repository = repository

    async def get_orders(self, page: int, size: int):
        projection = {"_id": False}

        result, total_items = await self._repository.find_all_paginated(
            {}, page, size, projection
        )
        total_pages = calculate_pages(total_items, size)

        return {
            "items": result,
            "total_items": total_items,
            "page": page,
            "total_pages": total_pages,
        }
