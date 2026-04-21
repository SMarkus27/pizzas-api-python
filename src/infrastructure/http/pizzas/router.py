from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.infrastructure.http.pizzas.dependencies import (
    get_create_pizza_use_case,
    get_delete_pizza_use_case,
    get_list_pizzas_use_case,
    get_pizza_use_case,
    get_update_pizza_use_case,
)
from src.infrastructure.http.pizzas.schemas import (
    CreatePizzaInSchema,
    UpdatePizzaInSchema,
)
from src.infrastructure.http.response import Response
from src.use_cases.pizzas.create import CreatePizzaUseCase
from src.use_cases.pizzas.delete import DeletePizzaUseCase
from src.use_cases.pizzas.get import GetPizzaUseCase, ListPizzasUseCase
from src.use_cases.pizzas.update import UpdatePizzaUseCase


router = APIRouter(prefix="/api/pizzas", tags=["Pizzas"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_pizza(
    data: CreatePizzaInSchema,
    use_case: Annotated[CreatePizzaUseCase, Depends(get_create_pizza_use_case)],
):
    result = await use_case.execute(data)
    return Response(data={"result": result}, status_code=status.HTTP_201_CREATED)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_pizzas(
    use_case: Annotated[ListPizzasUseCase, Depends(get_list_pizzas_use_case)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query()] = 10,
):
    result = await use_case.get_all(page, size)
    return Response(data=result, status_code=status.HTTP_200_OK)


@router.get("/{pizza_external_id}", status_code=status.HTTP_200_OK)
async def get_one_pizza(
    pizza_external_id: str,
    use_case: Annotated[GetPizzaUseCase, Depends(get_pizza_use_case)],
):
    result = await use_case.get_one(pizza_external_id)
    return Response(data={"result": result}, status_code=status.HTTP_200_OK)


@router.patch("/{pizza_external_id}", status_code=status.HTTP_200_OK)
async def update_pizza(
    pizza_external_id: str,
    data: UpdatePizzaInSchema,
    use_case: Annotated[UpdatePizzaUseCase, Depends(get_update_pizza_use_case)],
):
    await use_case.execute(pizza_external_id, data)
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{pizza_external_id}", status_code=status.HTTP_200_OK)
async def delete_pizza(
    pizza_external_id: str,
    use_case: Annotated[DeletePizzaUseCase, Depends(get_delete_pizza_use_case)],
):
    await use_case.execute(pizza_external_id)
    return Response(status_code=status.HTTP_200_OK)
