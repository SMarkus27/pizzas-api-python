from fastapi import APIRouter


class BaseRouter:
    has_router: APIRouter = None

    @classmethod
    def get_router_instance(cls):
        if cls.has_router is None:
            cls.has_router = APIRouter()
        return cls.has_router
