from typing import Any


class FakeRepository:
    def __init__(self):
        self._data: dict[str, dict[str, str]] = {}

    async def insert_one(self, data: dict[str, Any]) -> None:
        self._data[data["external_id"]] = data

    async def find_one(
        self, query: dict[str, Any], _projection: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        name = query.get("name")
        external_id = query.get("external_id")

        for item in self._data.values():
            if name and item["name"] == name:
                return item

            if external_id and item["external_id"] == external_id:
                return item

        return None

    async def update_one(
        self,
        query: dict[str, Any],
        new_data: dict[str, Any],
        _array_filters: list[dict[str, Any]] | None = None,
        _upsert: bool = False,
    ) -> None:
        item = await self.find_one(query)
        if item:
            self._data[item["external_id"]].update(new_data)

    async def delete_one(self, query: dict[str, Any]) -> None:
        item = await self.find_one(query)
        if item:
            del self._data[item["external_id"]]

    async def find_all_paginated(
        self,
        _query: dict[
            str, Any
        ],  # Prefixed with _ as it's not fully used in this fake implementation
        page: int,
        limit: int,
        _projection: dict[str, Any] | None = None,  # Prefixed with _
        _sort: tuple | None = None,  # Prefixed with _
    ) -> tuple[list[dict[str, Any]], int]:
        items = list(self._data.values())
        total_items = len(items)

        skip = (page - 1) * limit
        return items[skip : skip + limit], total_items
