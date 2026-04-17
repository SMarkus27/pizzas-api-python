from src.core.exceptions import NotFoundError
from src.core.protocols.repository import BaseRepositoryProtocol


class GetOrderService:
    def __init__(self, repository: BaseRepositoryProtocol):
        self._repository = repository

    async def get_order(self, external_id: str) -> dict:
        query = {"external_id": external_id}
        result = await self._repository.find_one(query, {"_id": False})
        if not result:
            raise NotFoundError()

        return result
