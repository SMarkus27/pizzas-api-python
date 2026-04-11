from src.core.exceptions import NotFoundException
from src.repositories.orders.repository import OrderRepository



class GetOrderService:

    def __init__(self, repository: OrderRepository):
        self._repository = repository

    async def get_order(self, external_id: str):
        query = {"external_id": external_id}
        result = await self._repository.find_one(query, {"_id": False})
        if not result:
            raise NotFoundException()

        return result
