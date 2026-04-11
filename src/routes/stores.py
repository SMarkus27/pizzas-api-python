from fastapi import APIRouter
from fastapi.params import Depends, Query
from fastapi import status

from src.services.stores.dependencies import get_create_store_service, get_all_store_service, get_update_store_service
from src.domain.common.response import Response
from src.domain.models.store.model import CreateStoreInSchema
from src.services.stores.create.service import CreateStoreService
from src.services.stores.get_all.service import GetAllStoreService
from src.services.stores.update.service import UpdateStoreService

router = APIRouter(prefix="/api/stores", tags=["Stores"])

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_store_item(data: CreateStoreInSchema, service: CreateStoreService = Depends(get_create_store_service)):
    data = await service.create(data)
    return Response(data={"result": data}, status_code=status.HTTP_201_CREATED)

@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_store_items(page: int = Query(1), size: int =  Query(10), service: GetAllStoreService = Depends(get_all_store_service)):
    data = await service.get_all(page, size)
    return Response(data={"result": data}, status_code=status.HTTP_200_OK)

@router.put("/", status_code=status.HTTP_200_OK)
async def update_store_item(data: CreateStoreInSchema, service: UpdateStoreService = Depends(get_update_store_service)):
    await service.update(data)
    return Response(data={"result": data}, status_code=status.HTTP_200_OK)
