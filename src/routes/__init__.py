from fastapi import FastAPI

from src.routes.orders import router as orders_routes
from src.routes.pizzas import router as pizza_routes
from src.routes.stores import router as store_routes


def register_routes(app: FastAPI):
    app.include_router(pizza_routes)
    app.include_router(store_routes)
    app.include_router(orders_routes)
