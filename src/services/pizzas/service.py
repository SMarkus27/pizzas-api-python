from datetime import datetime

from src.core.interfaces.services.pizzas.interface import IPizzaService
from src.repositories.pizzas.repository import PizzasRepository


class PizzaService(IPizzaService):

    @classmethod
    async def create_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        data = payload.get("payload")
        pizza_name = data.get("name")
        query = {"name": pizza_name}
        projection = {"_id": False}
        pizza_data = await pizza_repo.find_one(query, projection)

        if pizza_data:
            return {
                "status_code": 200,
                "message": "Pizza already exist!. Try another pizza"
            }

        data.update({"created_at": datetime.now()})
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
            "result": result,
            "status_code": 200,
            "message": "",
        }

    @classmethod
    async def find_one_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        pizza_name = payload.get("pizza_name")
        query = {"name": {"$regex": pizza_name, "$options": "i"}}

        result = await pizza_repo.find_one(query, projection)
        if not result:
            return {
                "result": [],
                "status_code": 404,
                "message": "Pizza not found",
            }

        return {
            "result": result,
            "status_code": 200,
            "message": "",
        }

    @classmethod
    async def update_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        pizza_name = payload.get("pizza_name")
        query = {"name": pizza_name}
        projection = {"_id": False}
        new_data = payload.get("data")
        new_data.update({"updated_at": datetime.now()})

        result = await pizza_repo.find_one(query, projection)
        if not result:
            return {
                "result": [],
                "status_code": 404,
                "message": "Pizza not found",
            }

        await pizza_repo.update_one(query, new_data)
        return {
            "result": [],
            "status_code": 200,
            "message": "Pizza Created",
        }

    @classmethod
    async def delete_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        pizza_name = payload.get("pizza_name")
        query = {"name": pizza_name}
        projection = {"_id": False}

        result = await pizza_repo.find_one(query, projection)
        if not result:
            return {
                "result": [],
                "status_code": 404,
                "message": "Pizza not found",
            }
        await pizza_repo.delete_one(query)
        return {
            "result": [],
            "status_code": 200,
            "message": "Pizza Deleted"
        }
