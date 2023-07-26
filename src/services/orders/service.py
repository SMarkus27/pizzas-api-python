from datetime import datetime
from uuid import uuid4

from fastapi import status

from src.domain.models.responses.base.model import BaseResponse
from src.repositories.orders.repository import OrderRepository
from src.repositories.pizzas.repository import PizzasRepository
from src.repositories.store.repository import StoreRepository
from src.services.store.service import StoreService


class OrderService:

    @classmethod
    async def get_orders(cls, payload: dict, order_repo=OrderRepository):
        projection = {"_id": False}
        result = await order_repo.find_all({}, projection)

        response = BaseResponse(
            result=result,
            status_code=status.HTTP_302_FOUND,
            message="All orders"

        ).__dict__
        return response

    @classmethod
    async def get_order(cls, payload: dict, order_repo=OrderRepository):
        order_id = payload.get("order_id")

        query = {"order_id": order_id}
        result = await order_repo.find_one(query, {"_id": False})
        if not result:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_404_NOT_FOUND,
                message="Order not found"
            ).__dict__

        return BaseResponse(
            result=result,
            status_code=status.HTTP_200_OK,
            message="Order info"
        ).__dict__

    @classmethod
    async def get_pizza(cls, payload: dict, order_repo=OrderRepository, store_repo=StoreRepository, pizza_repo=PizzasRepository):
        order_data = payload.get("order_data")
        order_quantity = order_data.get("quantity")
        pizza_name = order_data.get("name")
        query = {"name": pizza_name}

        quantity = order_data.get("quantity")
        if quantity <= 0:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid Quantity: {quantity}. Quantity must be greater than zero"
            }

        result = await store_repo.find_one(query, {"_id": False})

        if not result:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_404_NOT_FOUND,
                message="Item not found"
            ).__dict__

        store_quantity = result.get("quantity")

        if store_quantity < order_quantity:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_200_OK,
                message="Item store is lower"
            ).__dict__

        payload = {"payload": order_data}
        await StoreService.reduce_item_store(payload)

        pizza_data = await pizza_repo.find_one(query, {"_id": False})
        pizza_price = pizza_data.get("price")

        order_data.update({"created_at": datetime.now().isoformat(),
                           "price": pizza_price * order_quantity,
                           "order_id": str(uuid4())})

        await order_repo.insert_one(order_data)
        order_data.pop("_id")
        return BaseResponse(
            result=order_data,
            status_code=status.HTTP_200_OK,
            message="Order receive"
        ).__dict__
