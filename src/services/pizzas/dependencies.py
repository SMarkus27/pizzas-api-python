from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.repositories.pizzas.repository import PizzaRepository
from src.services.pizzas.create.service import CreatePizzaService
from src.services.pizzas.delete.service import DeletePizzaService
from src.services.pizzas.get.service import GetPizzaService
from src.services.pizzas.get_all.service import GetAllPizzaService
from src.services.pizzas.update.service import UpdatePizzaService


def get_pizza_repo(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> PizzaRepository:
    return PizzaRepository(db)


def get_create_pizza_service(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repo)],
) -> CreatePizzaService:
    return CreatePizzaService(repository)


def get_all_pizza_service(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repo)],
) -> GetAllPizzaService:
    return GetAllPizzaService(repository)


def get_get_pizza_service(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repo)],
) -> GetPizzaService:
    return GetPizzaService(repository)


def get_update_pizza_service(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repo)],
) -> UpdatePizzaService:
    return UpdatePizzaService(repository)


def get_delete_pizza_service(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repo)],
) -> DeletePizzaService:
    return DeletePizzaService(repository)
