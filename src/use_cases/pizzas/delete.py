from src.domain.exceptions import NotFoundError
from src.domain.repositories.base import BaseRepositoryProtocol


class DeletePizzaUseCase:
    def __init__(self, repository: BaseRepositoryProtocol) -> None:
        self._repository = repository

    async def execute(self, pizza_external_id: str) -> None:
        query = {"external_id": pizza_external_id}
        result = await self._repository.find_one(query)

        if not result:
            raise NotFoundError()

        await self._repository.delete_one(query)
