from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.infrastructure.mongodb.order_repository import OrderRepository
from src.infrastructure.mongodb.pizza_repository import PizzaRepository
from src.infrastructure.mongodb.store_repository import StoreRepository
from src.use_cases.orders.create import CreateOrderUseCase
from src.use_cases.orders.get import GetOrderUseCase, ListOrdersUseCase


def get_pizza_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> PizzaRepository:
    return PizzaRepository(db)


def get_store_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StoreRepository:
    return StoreRepository(db)


def get_order_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> OrderRepository:
    return OrderRepository(db)


def get_create_order_use_case(
    order_repository: Annotated[OrderRepository, Depends(get_order_repository)],
    store_repository: Annotated[StoreRepository, Depends(get_store_repository)],
    pizza_repository: Annotated[PizzaRepository, Depends(get_pizza_repository)],
) -> CreateOrderUseCase:
    return CreateOrderUseCase(order_repository, store_repository, pizza_repository)


def get_list_orders_use_case(
    repository: Annotated[OrderRepository, Depends(get_order_repository)],
) -> ListOrdersUseCase:
    return ListOrdersUseCase(repository)


def get_order_use_case(
    repository: Annotated[OrderRepository, Depends(get_order_repository)],
) -> GetOrderUseCase:
    return GetOrderUseCase(repository)
