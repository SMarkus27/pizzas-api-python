from abc import ABCMeta, abstractmethod

from src.repositories.store.repository import StoreRepository


class IStoreService(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @classmethod
    @abstractmethod
    async def add_item_store(cls, payload: dict, store_repo=StoreRepository):
        pass

    @classmethod
    @abstractmethod
    async def reduce_item_store(cls, payload: dict, store_repo=StoreRepository):
        pass

    @classmethod
    @abstractmethod
    async def get_all_items(cls, payload: dict, store_repo=StoreRepository):
        pass
