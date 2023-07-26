from src.controllers.base.controller import BaseController
from src.controllers.store.controller import StoreController
from src.domain.models.store.model import StoreModel
from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.post("/api/store/", tags=["store"])
async def add_item_store(store_data: StoreModel):
    return await BaseController.run(
        StoreController.add_item_store, {"payload": store_data.dict()})


@router.put("/api/store/", tags=["store"])
async def remove_item_store(store_data: StoreModel):
    return await BaseController.run(
        StoreController.remove_item_store, {"payload": store_data.dict()}
    )