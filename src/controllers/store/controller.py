from src.core.interfaces.controllers.store.interface import IStoreController
from src.services.store.service import StoreService


class StoreController(IStoreController):
    @staticmethod
    async def add_item_store(payload: dict):
        return await StoreService.add_item_store(payload)

    @staticmethod
    async def remove_item_store(payload: dict):
        return await StoreService.reduce_item_store(payload)

    @staticmethod
    async def get_all_items(payload: dict):
        return await StoreService.get_all_items(payload)
