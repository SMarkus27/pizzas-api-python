from math import ceil
from typing import Any

from motor.motor_asyncio import AsyncIOMotorDatabase


class BaseMongoDBRepository:
    def __init__(self, database: AsyncIOMotorDatabase, collection: str) -> None:
        self._collection = database[collection]

    async def insert_one(self, data: dict[str, Any]) -> None:
        await self._collection.insert_one(data)

    async def find_all(
        self,
        query: dict[str, Any],
        projection: dict[str, Any] | None = None,
        limit: int | None = None,
        sort: tuple | None = None,
    ) -> list[dict[str, Any]]:
        cursor = self._collection.find(query, projection)
        if sort:
            cursor.sort(*sort)

        if limit:
            cursor.limit(limit)
        return await cursor.to_list(limit)

    async def find_one(
        self, query: dict[str, Any], projection: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        return await self._collection.find_one(query, projection)

    async def update_one(
        self,
        query: dict[str, Any],
        new_data: dict[str, Any],
        array_filters: list[dict[str, Any]] | None = None,
        upsert: bool = False,
    ) -> None:
        new = {"$set": new_data}
        return await self._collection.update_one(
            query, new, array_filters=array_filters, upsert=upsert
        )

    async def delete_one(self, query: dict[str, Any]) -> None:
        return await self._collection.delete_one(query)

    async def find_all_paginated(
        self,
        query: dict[str, Any],
        page: int,
        limit: int,
        projection: dict[str, Any] | None = None,
        sort: tuple | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        total_items = await self._collection.count_documents(query)

        if not total_items:
            return [], 0

        skip = (page - 1) * limit
        cursor = self._collection.find(query, projection)
        if sort:
            cursor.sort(*sort)

        results = await cursor.skip(skip).limit(limit).to_list(limit)
        return results, total_items

    @staticmethod
    def calculate_pages(total_items: int, limit: int) -> int:
        return ceil(total_items / limit) if limit > 0 else 0
