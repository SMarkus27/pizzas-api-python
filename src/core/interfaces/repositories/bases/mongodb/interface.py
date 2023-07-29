from abc import ABCMeta, abstractmethod


class IBaseMongoDBRepo(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @classmethod
    @abstractmethod
    async def insert_one(cls, data: dict):
        pass

    @classmethod
    @abstractmethod
    async def find_all(
        cls, query: dict, limit: int = None, projection: dict = None, sort: tuple = None
    ):
        pass

    @classmethod
    @abstractmethod
    async def find_one(cls, query: dict, projection: dict):
        pass

    @classmethod
    @abstractmethod
    async def update_one(
        cls,
        query: dict,
        new_data: dict,
        array_filters: list = None,
        upsert: bool = False,
    ):
        pass

    @classmethod
    @abstractmethod
    async def delete_one(cls, query: dict):
        pass
