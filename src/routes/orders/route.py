from fastapi import Header

from src.controllers.base.controller import BaseController
from src.controllers.orders.controller import OrderController
from src.domain.models.orders.model import OrdersModel
from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.get("/api/orders", tags=["orders"])
async def get_orders(size=Header(), page=Header()):
    return await BaseController.run(
        OrderController.get_orders, {"size": size, "page": page}
    )


@router.get("/api/orders/{order_id}", tags=["orders"])
async def get_order(order_id: str):
    return await BaseController.run(OrderController.get_order, {"order_id": order_id})


@router.post("/api/orders/", tags=["orders"])
async def get_pizza(order_data: OrdersModel):
    return await BaseController.run(
        OrderController.get_pizza, {"order_data": order_data.dict()}
    )
