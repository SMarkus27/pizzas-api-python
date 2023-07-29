from src.core.interfaces.controllers.orders.interface import IOrderController
from src.services.orders.service import OrderService


class OrderController(IOrderController):
    @staticmethod
    async def get_orders(payload: dict):
        return await OrderService.get_orders(payload)

    @staticmethod
    async def get_order(payload: dict):
        return await OrderService.get_order(payload)

    @staticmethod
    async def get_pizza(payload: dict):
        return await OrderService.get_pizza(payload)
