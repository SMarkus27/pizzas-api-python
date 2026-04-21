from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from src.infrastructure.http.response import Response
from src.infrastructure.http.stores.dependencies import (
    get_create_store_use_case,
    get_list_stores_use_case,
    get_update_store_use_case,
)
from src.infrastructure.http.stores.schemas import (
    CreateStoreInSchema,
    UpdateStoreInSchema,
)
from src.use_cases.stores.create import CreateStoreUseCase
from src.use_cases.stores.get import ListStoresUseCase
from src.use_cases.stores.update import UpdateStoreUseCase


router = APIRouter(prefix="/api/stores", tags=["Stores"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_store_item(
    data: CreateStoreInSchema,
    use_case: Annotated[CreateStoreUseCase, Depends(get_create_store_use_case)],
):
    result = await use_case.execute(data)
    return Response(data={"result": result}, status_code=status.HTTP_201_CREATED)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_store_items(
    use_case: Annotated[ListStoresUseCase, Depends(get_list_stores_use_case)],
    page: Annotated[int, Query(ge=1)] = 1,
    size: Annotated[int, Query()] = 10,
):
    result = await use_case.get_all(page, size)
    return Response(data=result, status_code=status.HTTP_200_OK)


@router.patch("/increase", status_code=status.HTTP_200_OK)
async def increase_store_item(
    data: UpdateStoreInSchema,
    use_case: Annotated[UpdateStoreUseCase, Depends(get_update_store_use_case)],
):
    await use_case.increase(data)
    return Response(
        data={"message": "Quantity increased successfully"},
        status_code=status.HTTP_200_OK,
    )


@router.patch("/decrease", status_code=status.HTTP_200_OK)
async def decrease_store_item(
    data: UpdateStoreInSchema,
    use_case: Annotated[UpdateStoreUseCase, Depends(get_update_store_use_case)],
):
    await use_case.decrease(data)
    return Response(
        data={"message": "Quantity decreased successfully"},
        status_code=status.HTTP_200_OK,
    )
