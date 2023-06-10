from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.get("/api/order")
async def get_orders():
    pass


@router.get("/api/order/{order_id}")
async def get_order(order_id: str):
    pass


@router.post("/api/order/")
async def get_pizza(order_data: dict):
    pass
