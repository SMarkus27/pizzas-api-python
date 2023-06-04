from src.routes.base.route import BaseRouter

router = BaseRouter.get_router_instance()


@router.post("api/pizzas/")
async def create_pizza(pizza_data: dict):
    return "hello"


@router.get("api/pizzas/")
async def get_all_pizzas():
    return "hello"


@router.get("api/pizzas/{pizza_id}")
async def get_one_pizza(pizza_id: str):
    return "hello"


@router.put("api/pizzas/{pizza_id}")
async def update_pizza(pizza_id: str, new_data: dict):
    return "hello"


@router.delete("api/pizzas/{pizza_id}")
async def delete_pizza(pizza_id: str):
    return "hello"
