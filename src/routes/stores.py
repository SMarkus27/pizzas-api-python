from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.domain.common.response import Response
from src.services.stores.create.schemas import CreateStoreInSchema
from src.services.stores.create.service import CreateStoreService
from src.services.stores.dependencies import (
    get_all_store_service,
    get_create_store_service,
    get_update_store_service,
)
from src.services.stores.get_all.service import GetAllStoreService
from src.services.stores.update.schemas import UpdateStoreInSchema
from src.services.stores.update.service import UpdateStoreService


router = APIRouter(prefix="/api/stores", tags=["Stores"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_store_item(
    data: CreateStoreInSchema,
    service: Annotated[CreateStoreService, Depends(get_create_store_service)],
):
    data = await service.create(data)
    return Response(data={"result": data}, status_code=status.HTTP_201_CREATED)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_store_items(
    service: Annotated[GetAllStoreService, Depends(get_all_store_service)],
    page: Annotated[int, Query()] = 1,
    size: Annotated[int, Query()] = 10,
):
    data = await service.get_all(page, size)
    return Response(data={"result": data}, status_code=status.HTTP_200_OK)


@router.patch("/increase", status_code=status.HTTP_200_OK)
async def increase_store_item(
    data: UpdateStoreInSchema,
    service: Annotated[UpdateStoreService, Depends(get_update_store_service)],
):
    await service.increase(data)
    return Response(
        data={"message": "Quantity increased successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.patch("/decrease", status_code=status.HTTP_200_OK)
async def decrease_store_item(
    data: UpdateStoreInSchema,
    service: Annotated[UpdateStoreService, Depends(get_update_store_service)],
):
    await service.decrease(data)
    return Response(
        data={"message": "Quantity decreased successfully"},
        status_code=status.HTTP_200_OK,
    )
