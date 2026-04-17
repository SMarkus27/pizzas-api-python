from src.core.exceptions import NotFoundError
from src.core.protocols.repository import BaseRepositoryProtocol


class GetPizzaService:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def get_one(self, pizza_external_id: str) -> dict:
        query = {"external_id": pizza_external_id}
        projection = {"_id": 0}

        result = await self._repository.find_one(query, projection)
        if not result:
            raise NotFoundError()

        return result
