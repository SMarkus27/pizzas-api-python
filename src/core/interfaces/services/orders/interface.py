from abc import ABCMeta, abstractmethod

from src.repositories.orders.repository import OrderRepository
from src.repositories.pizzas.repository import PizzasRepository
from src.repositories.store.repository import StoreRepository


class IOrderService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @classmethod
    @abstractmethod
    async def get_orders(cls, payload: dict, order_repo=OrderRepository):
        pass

    @classmethod
    @abstractmethod
    async def get_order(cls, payload: dict, order_repo=OrderRepository):
        pass

    @classmethod
    @abstractmethod
    async def get_pizza(
        cls,
        payload: dict,
        order_repo=OrderRepository,
        store_repo=StoreRepository,
        pizza_repo=PizzasRepository,
    ):
        pass
