from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.infrastructure.mongodb.store_repository import StoreRepository
from src.use_cases.stores.create import CreateStoreUseCase
from src.use_cases.stores.get import ListStoresUseCase
from src.use_cases.stores.update import UpdateStoreUseCase


def get_store_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StoreRepository:
    return StoreRepository(db)


def get_create_store_use_case(
    repository: Annotated[StoreRepository, Depends(get_store_repository)],
) -> CreateStoreUseCase:
    return CreateStoreUseCase(repository)


def get_list_stores_use_case(
    repository: Annotated[StoreRepository, Depends(get_store_repository)],
) -> ListStoresUseCase:
    return ListStoresUseCase(repository)


def get_update_store_use_case(
    repository: Annotated[StoreRepository, Depends(get_store_repository)],
) -> UpdateStoreUseCase:
    return UpdateStoreUseCase(repository)
