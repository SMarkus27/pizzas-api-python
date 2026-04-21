from fastapi import FastAPI

from src.infrastructure.http.orders.router import router as orders_router
from src.infrastructure.http.pizzas.router import router as pizzas_router
from src.infrastructure.http.stores.router import router as stores_router


def register_routes(app: FastAPI) -> None:
    app.include_router(pizzas_router)
    app.include_router(stores_router)
    app.include_router(orders_router)
