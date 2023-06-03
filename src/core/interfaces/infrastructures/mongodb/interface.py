from abc import ABCMeta, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient


class IMongoDBInfra(metaclass=ABCMeta):

    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @classmethod
    @abstractmethod
    def get_mongodb_client(cls) -> AsyncIOMotorClient:
        pass
