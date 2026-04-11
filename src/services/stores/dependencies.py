from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.repositories.store.repository import StoreRepository
from src.services.stores.create.service import CreateStoreService
from src.services.stores.get_all.service import GetAllStoreService
from src.services.stores.update.service import UpdateStoreService


def get_store_repo(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StoreRepository:
    return StoreRepository(db)


def get_create_store_service(
    repository: Annotated[StoreRepository, Depends(get_store_repo)],
) -> CreateStoreService:
    return CreateStoreService(repository)


def get_all_store_service(
    repository: Annotated[StoreRepository, Depends(get_store_repo)],
) -> GetAllStoreService:
    return GetAllStoreService(repository)


def get_update_store_service(
    repository: Annotated[StoreRepository, Depends(get_store_repo)],
) -> UpdateStoreService:
    return UpdateStoreService(repository)
