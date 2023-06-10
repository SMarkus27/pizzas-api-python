from src.controllers.base.controller import BaseController
from src.controllers.store.controller import StoreController
from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.post("/api/store/", tags=["store"])
async def add_item_store(store_data: dict):
    return await BaseController.run(
        StoreController.add_item_store, {"payload": store_data})


@router.put("/api/store/", tags=["store"])
async def remove_item_store(store_data: dict):
    return await BaseController.run(
        StoreController.remove_item_store, {"payload": store_data}
    )