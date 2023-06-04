from src.services.pizzas.service import PizzaService


class PizzasController:

    @staticmethod
    async def create_pizza(payload: dict):
        return await PizzaService.create_pizza(payload)

    @staticmethod
    async def get_all_pizzas(payload: dict):
        return await PizzaService.find_all_pizzas(payload)

    @staticmethod
    async def get_pizza(payload: dict):
        return await PizzaService.find_all_pizzas(payload)

    @staticmethod
    async def update_pizza(payload: dict):
        return await PizzaService.update_pizza(payload)

    @staticmethod
    async def delete_pizza(payload: dict):
        return await PizzaService.delete_pizza(payload)