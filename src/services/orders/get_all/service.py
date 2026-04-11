from src.repositories.orders.repository import OrderRepository


class GetAllOrderService:
    def __init__(self, repository: OrderRepository):
        self._repository = repository

    async def get_orders(self, page: int, size: int):
        projection = {"_id": False}

        result, total_items = await self._repository.find_all_paginated(
            {}, page, size, projection
        )
        total_pages = self._repository.calculate_pages(total_items, size)

        result = {
            "result": result,
            "total_items": total_items,
            "page": page,
            "total_pages": total_pages,
        }
        return result
