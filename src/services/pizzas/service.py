from datetime import datetime
from fastapi import status

from src.core.interfaces.services.pizzas.interface import IPizzaService
from src.domain.models.responses.base.model import BaseResponse
from src.domain.models.responses.orders.model import OrdersResponse
from src.repositories.pizzas.repository import PizzasRepository


class PizzaService(IPizzaService):

    @classmethod
    async def create_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        data = payload.get("payload")
        pizza_name = data.get("name")
        query = {"name": pizza_name}
        projection = {"_id": False}

        price = data.get("price")
        if price <= 0:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"Price invalid: {price}. Price must be greater than zero"
            }

        pizza_data = await pizza_repo.find_one(query, projection)

        if pizza_data:
            return {
                "status_code": status.HTTP_200_OK,
                "message": "Pizza already exist!. Try another pizza"
            }

        data.update({"created_at": datetime.now().isoformat()})
        await pizza_repo.insert_one(data)
        return {
            "status_code": status.HTTP_201_CREATED,
            "message": "Pizza created!"
        }

    @classmethod
    async def find_all_pizzas(cls, payload: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        limit = int(payload.get("size"))
        page = int(payload.get("page"))

        skip = pizza_repo.calculate_skip(limit, page)

        result, total_items = await pizza_repo.find_all_paginated({}, skip, limit, projection)
        total_pages = pizza_repo.calculate_pages(total_items, limit)

        response = OrdersResponse(
            result=result,
            total_pages=total_pages,
            status_code=status.HTTP_302_FOUND,
            message=""

        ).__dict__
        return response

    @classmethod
    async def find_one_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        projection = {"_id": False}
        pizza_name = payload.get("pizza_name")
        query = {"name": {"$regex": pizza_name, "$options": "i"}}

        result = await pizza_repo.find_one(query, projection)
        if not result:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_404_NOT_FOUND,
                message="Pizza not found",
            ).__dict__

        response = BaseResponse(
            result=result,
            status_code=status.HTTP_302_FOUND,
            message="Pizza Found"

        ).__dict__
        return response

    @classmethod
    async def update_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        pizza_name = payload.get("pizza_name")
        query = {"name": pizza_name}
        projection = {"_id": False}
        new_data = payload.get("data")
        new_data.update({"updated_at": datetime.now().isoformat()})

        price = new_data.get("price")
        if price <= 0:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"Price invalid: {price}. Price must be greater than zero"
            }

        result = await pizza_repo.find_one(query, projection)
        if not result:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_404_NOT_FOUND,
                message="Pizza not found",
            ).__dict__

        await pizza_repo.update_one(query, new_data)
        response = BaseResponse(
            result=[],
            status_code=status.HTTP_200_OK,
            message="Pizza updated"

        ).__dict__
        return response

    @classmethod
    async def delete_pizza(cls, payload: dict, pizza_repo=PizzasRepository):
        pizza_name = payload.get("pizza_name")
        query = {"name": pizza_name}
        projection = {"_id": False}

        result = await pizza_repo.find_one(query, projection)
        if not result:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_404_NOT_FOUND,
                message="Pizza not found",
            ).__dict__

        await pizza_repo.delete_one(query)
        response = BaseResponse(
            result=[],
            status_code=status.HTTP_200_OK,
            message="Pizza updated"

        ).__dict__
        return response
