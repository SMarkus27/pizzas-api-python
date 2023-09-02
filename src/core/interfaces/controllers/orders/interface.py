from abc import ABCMeta, abstractmethod


class IOrderController(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @staticmethod
    @abstractmethod
    async def get_orders(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def get_order(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def get_pizza(payload: dict):
        pass
