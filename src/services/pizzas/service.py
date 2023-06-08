from src.core.interfaces.services.pizzas.interface import IPizzaService
from src.repositories.pizzas.repository import PizzasRepository


class PizzaService(IPizzaService):

    @classmethod
    async def create_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        data = payload.get("payload")
        await pizza_repo.insert_one(data)
        return {
            "status_code": 201,
            "message": "Pizza created!"
        }

    @classmethod
    async def find_all_pizzas(cls, data: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        result = await pizza_repo.find_all(data, projection)
        return result

    @classmethod
    async def find_one_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        result = await pizza_repo.find_one(data, projection)
        return result

    @classmethod
    async def update_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        await pizza_repo.update_one(data, {})
        return "ok"

    @classmethod
    async def delete_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        await pizza_repo.delete_one(data)
        return "ok"
