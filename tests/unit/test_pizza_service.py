import pytest

from src.core.exceptions import ConflictError, NotFoundError
from src.services.pizzas.create.schemas import CreatePizzaInSchema
from src.services.pizzas.create.service import CreatePizzaService
from src.services.pizzas.delete.service import DeletePizzaService
from src.services.pizzas.get.service import GetPizzaService
from src.services.pizzas.update.schemas import UpdatePizzaInSchema
from src.services.pizzas.update.service import UpdatePizzaService


@pytest.mark.asyncio
async def test_create_pizza_success(pizza_repository):
    service = CreatePizzaService(pizza_repository)
    data = CreatePizzaInSchema(
        name="Margherita", price=30.0, ingredients=["tomato", "mozzarella"]
    )

    result = await service.create(data)

    assert "pizza_external_id" in result
    assert len(pizza_repository._data) == 1


@pytest.mark.asyncio
async def test_create_pizza_already_exists_fails(pizza_repository, create_pizza):
    _ = create_pizza
    data = CreatePizzaInSchema(
        name="Margherita", price=30.0, ingredients=["tomato", "mozzarella"]
    )
    service = CreatePizzaService(pizza_repository)

    with pytest.raises(ConflictError):
        await service.create(data)

    assert len(pizza_repository._data) == 1


@pytest.mark.asyncio
async def test_get_pizza_success(pizza_repository, create_pizza):
    _ = create_pizza
    service = GetPizzaService(pizza_repository)
    result = await service.get_one("123")

    assert result.get("name") == "Margherita"
    assert result.get("price") == 30.0
    assert result.get("ingredients") == ["tomato", "mozzarella"]


@pytest.mark.asyncio
async def test_get_pizza_not_found_fails(pizza_repository, create_pizza):
    _ = create_pizza
    service = GetPizzaService(pizza_repository)
    with pytest.raises(NotFoundError):
        await service.get_one("invalid_id")


@pytest.mark.asyncio
async def test_update_pizza_success(pizza_repository, create_pizza):
    _ = create_pizza
    service = UpdatePizzaService(pizza_repository)
    data = UpdatePizzaInSchema(name="Margherita 2")

    await service.update("123", data)

    pizza = await pizza_repository.find_one({"external_id": "123"})

    assert pizza["name"] == "Margherita 2"
    assert pizza["price"] == 30.0
    assert pizza["ingredients"] == ["tomato", "mozzarella"]


@pytest.mark.asyncio
async def test_delete_pizza_success(pizza_repository, create_pizza):
    _ = create_pizza
    service = DeletePizzaService(pizza_repository)
    await service.delete("123")

    assert len(pizza_repository._data) == 0
