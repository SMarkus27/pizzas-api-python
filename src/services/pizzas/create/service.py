from src.core.exceptions import ConflictError
from src.domain.models.pizza.create import CreatePizzaInSchema
from src.infrastructure.documents.pizza import PizzaDocument
from src.repositories.pizzas.repository import PizzaRepository


class CreatePizzaService:
    def __init__(self, repository: PizzaRepository) -> None:
        self._repository = repository

    async def create(self, data: CreatePizzaInSchema):
        query = {"name": data.name}

        pizza_data = await self._repository.find_one(query)

        if pizza_data:
            raise ConflictError("Pizza already exist!. Try another pizza")

        pizza = PizzaDocument(
            name=data.name, price=data.price, ingredients=data.ingredients
        )

        await self._repository.insert_one(pizza.to_dict())
        return {"pizza_external_id": pizza.external_id}
