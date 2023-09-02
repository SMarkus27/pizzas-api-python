from abc import abstractmethod, ABCMeta


class IStoreController(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @staticmethod
    @abstractmethod
    async def add_item_store(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def remove_item_store(payload: dict):
        pass

    @staticmethod
    @abstractmethod
    async def get_all_items(payload: dict):
        pass
