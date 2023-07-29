from abc import abstractmethod, ABCMeta


class IBaseController(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return True

    @staticmethod
    @abstractmethod
    async def run(callback: callable, payload: dict):
        pass
