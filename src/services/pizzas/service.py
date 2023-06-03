from src.core.interfaces.services.pizzas.interface import IPizzaService
from src.repositories.pizzas.repository import PizzasRepository


class PizzaService(IPizzaService):

    @classmethod
    async def create_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        await pizza_repo.insert_one(data)
        return "Ok"

    @classmethod
    async def find_all_pizzas(cls, query: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        result = await pizza_repo.find_all(query, projection)
        return result

    @classmethod
    async def find_one_pizza(cls, query: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        result = await pizza_repo.find_one(query, projection)
        return result

    @classmethod
    async def update_pizza(cls, query: dict, new_data: dict, pizza_repo=PizzasRepository):
        await pizza_repo.update_one(query, new_data)
        return "ok"

    @classmethod
    async def delete_pizza(cls, query: dict, pizza_repo=PizzasRepository):
        await pizza_repo.delete_one(query)
        return "ok"
