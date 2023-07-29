from abc import ABCMeta, abstractmethod


class IPizzasController(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @staticmethod
    @abstractmethod
    async def create_pizza(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def get_all_pizzas(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def get_pizza(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def update_pizza(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def delete_pizza(payload: dict):
        pass
