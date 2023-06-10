from src.services.store.service import StoreService


class StoreController:

    @staticmethod
    async def add_item_store(payload: dict):
        return await StoreService.add_item_store(payload)

    @staticmethod
    async def remove_item_store(payload: dict):
        return await StoreService.reduce_item_store(payload)
