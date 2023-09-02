from abc import ABCMeta, abstractmethod

from src.repositories.pizzas.repository import PizzasRepository


class IPizzaService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @classmethod
    @abstractmethod
    async def create_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        pass

    @classmethod
    @abstractmethod
    async def find_all_pizzas(cls, data: dict, pizza_repo=PizzasRepository):
        pass

    @classmethod
    @abstractmethod
    async def find_one_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        pass

    @classmethod
    @abstractmethod
    async def update_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        pass

    @classmethod
    @abstractmethod
    async def delete_pizza(cls, data: dict, pizza_repo=PizzasRepository):
        pass
