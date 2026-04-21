from typing import Annotated

from fastapi import Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.infrastructure.mongodb.client import get_db
from src.infrastructure.mongodb.pizza_repository import PizzaRepository
from src.use_cases.pizzas.create import CreatePizzaUseCase
from src.use_cases.pizzas.delete import DeletePizzaUseCase
from src.use_cases.pizzas.get import GetPizzaUseCase, ListPizzasUseCase
from src.use_cases.pizzas.update import UpdatePizzaUseCase


def get_pizza_repository(
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> PizzaRepository:
    return PizzaRepository(db)


def get_create_pizza_use_case(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repository)],
) -> CreatePizzaUseCase:
    return CreatePizzaUseCase(repository)


def get_list_pizzas_use_case(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repository)],
) -> ListPizzasUseCase:
    return ListPizzasUseCase(repository)


def get_pizza_use_case(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repository)],
) -> GetPizzaUseCase:
    return GetPizzaUseCase(repository)


def get_update_pizza_use_case(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repository)],
) -> UpdatePizzaUseCase:
    return UpdatePizzaUseCase(repository)


def get_delete_pizza_use_case(
    repository: Annotated[PizzaRepository, Depends(get_pizza_repository)],
) -> DeletePizzaUseCase:
    return DeletePizzaUseCase(repository)
