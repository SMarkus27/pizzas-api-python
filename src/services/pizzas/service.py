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
    async def find_all_pizzas(cls, payload: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        result = await pizza_repo.find_all({}, projection)
        return {
            "status_code": 200,
            "message":"",
            "result": result
        }

    @classmethod
    async def find_one_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        pizza_name = payload.get("pizza_name")
        query = {"name": {"$regex": pizza_name, "$options": "i"}}
        result = await pizza_repo.find_one(query, projection)
        return result

    @classmethod
    async def update_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        pizza_name = payload.get("pizza_name")
        query = {"name": pizza_name}
        new_data = payload.get("data")
        await pizza_repo.update_one(query, new_data)
        return "ok"

    @classmethod
    async def delete_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        pizza_name = payload.get("pizza_name")
        query = {"name": pizza_name}
        await pizza_repo.delete_one(query)
        return "ok"
