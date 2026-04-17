from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.domain.common.response import Response
from src.services.pizzas.create.schemas import CreatePizzaInSchema
from src.services.pizzas.create.service import CreatePizzaService
from src.services.pizzas.delete.service import DeletePizzaService
from src.services.pizzas.dependencies import (
    get_all_pizza_service,
    get_create_pizza_service,
    get_delete_pizza_service,
    get_get_pizza_service,
    get_update_pizza_service,
)
from src.services.pizzas.get.service import GetPizzaService
from src.services.pizzas.get_all.service import GetAllPizzaService
from src.services.pizzas.update.schemas import UpdatePizzaInSchema
from src.services.pizzas.update.service import UpdatePizzaService


router = APIRouter(prefix="/api/pizzas", tags=["Pizzas"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pizza(
    data: CreatePizzaInSchema,
    service: Annotated[CreatePizzaService, Depends(get_create_pizza_service)],
):
    result = await service.create(data)
    return Response(data={"result": result}, status_code=status.HTTP_201_CREATED)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_pizzas(
    service: Annotated[GetAllPizzaService, Depends(get_all_pizza_service)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query()] = 10,
):
    result = await service.get_all(page, size)
    return Response(data=result, status_code=status.HTTP_200_OK)


@router.get("/{pizza_external_id}", status_code=status.HTTP_200_OK)
async def get_one_pizza(
    pizza_external_id: str,
    service: Annotated[GetPizzaService, Depends(get_get_pizza_service)],
):
    result = await service.get_one(pizza_external_id)
    return Response(data={"result": result}, status_code=status.HTTP_200_OK)


@router.patch("/{pizza_external_id}", status_code=status.HTTP_200_OK)
async def update_pizza(
    pizza_external_id: str,
    data: UpdatePizzaInSchema,
    service: Annotated[UpdatePizzaService, Depends(get_update_pizza_service)],
):
    await service.update(pizza_external_id, data)
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{pizza_external_id}", status_code=status.HTTP_200_OK)
async def delete_pizza(
    pizza_external_id: str,
    service: Annotated[DeletePizzaService, Depends(get_delete_pizza_service)],
):
    await service.delete(pizza_external_id)
    return Response(status_code=status.HTTP_200_OK)
