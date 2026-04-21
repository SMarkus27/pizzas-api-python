from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.infrastructure.http.orders.dependencies import (
    get_create_order_use_case,
    get_list_orders_use_case,
    get_order_use_case,
)
from src.infrastructure.http.orders.schemas import CreateOrderInSchema
from src.infrastructure.http.response import Response
from src.use_cases.orders.create import CreateOrderUseCase
from src.use_cases.orders.get import GetOrderUseCase, ListOrdersUseCase


router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    data: CreateOrderInSchema,
    use_case: Annotated[CreateOrderUseCase, Depends(get_create_order_use_case)],
):
    result = await use_case.execute(data)
    return Response(data={"result": result}, status_code=status.HTTP_201_CREATED)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(
    use_case: Annotated[ListOrdersUseCase, Depends(get_list_orders_use_case)],
    page: Annotated[int, Query()] = 1,
    size: Annotated[int, Query()] = 10,
):
    data = await use_case.get_all(page, size)
    return Response(data=data, status_code=status.HTTP_200_OK)


@router.get("/{external_id}", status_code=status.HTTP_200_OK)
async def get_order(
    external_id: str,
    use_case: Annotated[GetOrderUseCase, Depends(get_order_use_case)],
):
    data = await use_case.get_one(external_id)
    return Response(data={"result": data}, status_code=status.HTTP_200_OK)
