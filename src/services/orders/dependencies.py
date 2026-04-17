from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.repositories.orders.repository import OrderRepository
from src.repositories.pizzas.repository import PizzaRepository
from src.repositories.store.repository import StoreRepository
from src.services.orders.create.service import CreateOrderService
from src.services.orders.get_all.service import GetAllOrderService
from src.services.orders.get_one.service import GetOrderService


def get_pizza_repo(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> PizzaRepository:
    return PizzaRepository(db)


def get_store_repo(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StoreRepository:
    return StoreRepository(db)


def get_order_repo(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> OrderRepository:
    return OrderRepository(db)


def get_create_order_service(
    order_repo: Annotated[OrderRepository, Depends(get_order_repo)],
    store_repo: Annotated[StoreRepository, Depends(get_store_repo)],
    pizza_repo: Annotated[PizzaRepository, Depends(get_pizza_repo)],
) -> CreateOrderService:
    return CreateOrderService(order_repo, store_repo, pizza_repo)


def get_all_order_service(
    order_repo: Annotated[OrderRepository, Depends(get_order_repo)],
) -> GetAllOrderService:
    return GetAllOrderService(order_repo)


def get_order_service(
    order_repo: Annotated[OrderRepository, Depends(get_order_repo)],
) -> GetOrderService:
    return GetOrderService(order_repo)
