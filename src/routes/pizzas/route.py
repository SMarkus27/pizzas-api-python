from src.controllers.base.controller import BaseController
from src.controllers.pizzas.controller import PizzasController
from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.post("/api/pizzas/")
async def create_pizza(pizza_data: dict):
    return await BaseController.run(
        PizzasController.create_pizza, {"payload": pizza_data})


@router.get("api/pizzas/")
async def get_all_pizzas():
    return await BaseController.run(
        PizzasController.get_all_pizzas,{}
    )


@router.get("api/pizzas/{pizza_id}")
async def get_one_pizza(pizza_id: str):
    return await BaseController.run(
        PizzasController.get_pizza, {"pizza_id": pizza_id}
    )


@router.put("api/pizzas/{pizza_id}")
async def update_pizza(pizza_id: str, new_data: dict):
    return await BaseController.run(
        PizzasController.get_all_pizzas, {"pizza_id": pizza_id, "data": new_data}
    )


@router.delete("api/pizzas/{pizza_id}")
async def delete_pizza(pizza_id: str):
    return await BaseController.run(
        PizzasController.get_all_pizzas, {"pizza_id": pizza_id}
    )
