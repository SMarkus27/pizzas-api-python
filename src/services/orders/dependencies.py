from fastapi.params import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.repositories.orders.repository import OrderRepository
from src.repositories.pizzas.repository import PizzaRepository
from src.repositories.store.repository import StoreRepository
from src.services.orders.create.service import CreateOrderService
from src.services.orders.get_all.service import GetAllOrderService
from src.services.orders.get_one.service import GetOrderService
from src.services.stores.update.service import UpdateStoreService


def get_pizza_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> PizzaRepository:
    return PizzaRepository(db)

def get_store_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> StoreRepository:
    return StoreRepository(db)

def get_order_repo(db: AsyncIOMotorDatabase = Depends(get_db)) -> OrderRepository:
    return OrderRepository(db)

def get_update_store_service(
    store_repo: StoreRepository = Depends(get_store_repo)
) -> UpdateStoreService:
    return UpdateStoreService(store_repo)


def get_create_order_service(
        order_repo: OrderRepository = Depends(get_order_repo),
        store_repo: StoreRepository = Depends(get_store_repo),
        pizza_repo: PizzaRepository = Depends(get_pizza_repo),
        update_store_service: UpdateStoreService = Depends(get_update_store_service),
) -> CreateOrderService:
    return CreateOrderService(order_repo, store_repo, pizza_repo, update_store_service)

def get_all_order_service(order_repo: OrderRepository = Depends(get_order_repo)) -> GetAllOrderService:
    return GetAllOrderService(order_repo)

def get_order_service(order_repo: OrderRepository = Depends(get_order_repo)) -> GetOrderService:
    return GetOrderService(order_repo)
