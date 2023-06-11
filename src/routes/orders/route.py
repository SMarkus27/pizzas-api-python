from src.controllers.base.controller import BaseController
from src.controllers.orders.controller import OrderController
from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.get("/api/order", tags=["orders"])
async def get_orders():
    return await BaseController.run(
        OrderController.get_orders, {}
    )


@router.get("/api/order/{order_id}", tags=["orders"])
async def get_order(order_id: str):
    return await BaseController.run(
        OrderController.get_order, {"order_id": order_id}
    )


@router.post("/api/order/", tags=["orders"])
async def get_pizza(order_data: dict):
    return await BaseController.run(
        OrderController.get_pizza, {"order_data": order_data}
    )
