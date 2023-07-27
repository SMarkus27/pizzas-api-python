from datetime import datetime

from fastapi import status

from src.domain.models.responses.base.model import BaseResponse
from src.domain.models.responses.store.model import StoreResponse
from src.repositories.store.repository import StoreRepository


class StoreService:

    @classmethod
    async def add_item_store(cls, payload: dict, store_repo=StoreRepository):
        store_data = payload.get("payload")
        pizza_name = store_data.get("name")
        query = {"name": pizza_name}
        projection = {"_id": False}

        quantity = store_data.get("quantity")
        if quantity <= 0:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid Quantity: {quantity}. Quantity must be greater than zero"
            }

        result = await store_repo.find_one(query, projection)
        if not result:
            store_data.update({"created_at": datetime.now().isoformat()})
            await store_repo.insert_one(store_data)
            return BaseResponse(
                result=[],
                status_code=status.HTTP_201_CREATED,
                message="Item stored"
            ).__dict__

        old_quantity = result.get("quantity")
        new_quantity = old_quantity + store_data["quantity"]

        await store_repo.update_one(query, {"quantity": new_quantity,
                                            "updated_at": datetime.now().isoformat()})
        return BaseResponse(
                result=[],
                status_code=status.HTTP_201_CREATED,
                message="Item stored"
            ).__dict__

    @classmethod
    async def reduce_item_store(cls, payload: dict, store_repo=StoreRepository):
        store_data = payload.get("payload")

        pizza_name = store_data.get("name")
        query = {"name": pizza_name}
        projection = {"_id": False}

        quantity = store_data.get("quantity")
        if quantity <= 0:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid Quantity: {quantity}. Quantity must be greater than zero"
            }

        result = await store_repo.find_one(query, projection)
        if not result:
            return BaseResponse(
                result=[],
                status_code=status.HTTP_404_NOT_FOUND,
                message="Item not found"
            ).__dict__

        old_quantity = result.get("quantity")
        if old_quantity == 0:
            return BaseResponse(
                    result=[],
                    status_code=status.HTTP_200_OK,
                    message="Item empty"
                ).__dict__

        if quantity > old_quantity:
            return {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "message": f"Invalid Quantity: {quantity}. Quantity limit must be less than {old_quantity}"
            }

        new_quantity = old_quantity - quantity

        await store_repo.update_one(query, {"quantity": new_quantity,
                                            "updated_at": datetime.now().isoformat()})

        return BaseResponse(
            result=[],
            status_code=status.HTTP_201_CREATED,
            message="Store Updated"
        ).__dict__

    @classmethod
    async def get_all_items(cls, payload: dict, store_repo=StoreRepository):
        projection = {"_id": False}
        limit = int(payload.get("size"))
        page = int(payload.get("page"))

        skip = store_repo.calculate_skip(limit, page)

        result, total_items = await store_repo.find_all_paginated({}, skip, limit, projection)
        total_pages = store_repo.calculate_pages(total_items, limit)

        response = StoreResponse(
            result=result,
            total_pages=total_pages,
            status_code=status.HTTP_302_FOUND,
            message=""

        ).__dict__
        return response
