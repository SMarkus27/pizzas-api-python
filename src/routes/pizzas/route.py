from fastapi import Header

from src.controllers.base.controller import BaseController
from src.controllers.pizzas.controller import PizzasController
from src.domain.models.pizza.model import PizzaModel
from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.post("/api/pizzas/", tags=["Pizzas"])
async def create_pizza(pizza_data: PizzaModel):
    return await BaseController.run(
        PizzasController.create_pizza, {"payload": pizza_data.dict()})


@router.get("/api/pizzas/", tags=["Pizzas"])
async def get_all_pizzas(size=Header(), page=Header()):
    return await BaseController.run(
        PizzasController.get_all_pizzas, {"size": size, "page": page}
    )


@router.get("/api/pizzas/{pizza_name}", tags=["Pizzas"])
async def get_one_pizza(pizza_name: str):
    return await BaseController.run(
        PizzasController.get_pizza, {"pizza_name": pizza_name}
    )


@router.put("/api/pizzas/{pizza_name}", tags=["Pizzas"])
async def update_pizza(pizza_name: str, new_data: PizzaModel):
    return await BaseController.run(
        PizzasController.update_pizza, {"pizza_name": pizza_name, "data": new_data.dict()}
    )


@router.delete("/api/pizzas/{pizza_id}", tags=["Pizzas"])
async def delete_pizza(pizza_id: str):
    return await BaseController.run(
        PizzasController.delete_pizza, {"pizza_name": pizza_id}
    )
