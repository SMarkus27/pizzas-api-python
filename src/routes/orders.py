from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.domain.common.response import Response
from src.services.orders.create.schemas import CreateOrderInSchema
from src.services.orders.create.service import CreateOrderService
from src.services.orders.dependencies import (
    get_all_order_service,
    get_create_order_service,
    get_order_service,
)
from src.services.orders.get_all.service import GetAllOrderService
from src.services.orders.get_one.service import GetOrderService


router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    data: CreateOrderInSchema,
    service: Annotated[CreateOrderService, Depends(get_create_order_service)],
):
    data = await service.create(data)
    return Response(data={"result": data}, status_code=status.HTTP_201_CREATED)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(
    service: Annotated[GetAllOrderService, Depends(get_all_order_service)],
    page: Annotated[int, Query()] = 1,
    size: Annotated[int, Query()] = 10,
):
    data = await service.get_orders(page, size)
    return Response(data=data, status_code=status.HTTP_200_OK)


@router.get("/{external_id}", status_code=status.HTTP_200_OK)
async def get_order(
    external_id: str,
    service: Annotated[GetOrderService, Depends(get_order_service)],
):
    data = await service.get_order(external_id)
    return Response(data={"result": data}, status_code=status.HTTP_200_OK)
