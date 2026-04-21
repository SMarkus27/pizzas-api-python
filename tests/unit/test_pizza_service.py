import pytest

from src.domain.exceptions import ConflictError, NotFoundError
from src.infrastructure.http.pizzas.schemas import CreatePizzaInSchema, UpdatePizzaInSchema
from src.use_cases.pizzas.create import CreatePizzaUseCase
from src.use_cases.pizzas.delete import DeletePizzaUseCase
from src.use_cases.pizzas.get import GetPizzaUseCase
from src.use_cases.pizzas.update import UpdatePizzaUseCase


@pytest.mark.asyncio
async def test_create_pizza_success(pizza_repository):
    service = CreatePizzaUseCase(pizza_repository)
    data = CreatePizzaInSchema(
        name="Margherita", price=30.0, ingredients=["tomato", "mozzarella"]
    )

    result = await service.execute(data)

    assert "pizza_external_id" in result
    assert len(pizza_repository._data) == 1


@pytest.mark.asyncio
async def test_create_pizza_already_exists_fails(pizza_repository, create_pizza):
    _ = create_pizza
    data = CreatePizzaInSchema(
        name="Margherita", price=30.0, ingredients=["tomato", "mozzarella"]
    )
    service = CreatePizzaUseCase(pizza_repository)

    with pytest.raises(ConflictError):
        await service.execute(data)

    assert len(pizza_repository._data) == 1


@pytest.mark.asyncio
async def test_get_pizza_success(pizza_repository, create_pizza):
    _ = create_pizza
    service = GetPizzaUseCase(pizza_repository)
    result = await service.get_one("123")

    assert result.get("name") == "Margherita"
    assert result.get("price") == 30.0
    assert result.get("ingredients") == ["tomato", "mozzarella"]


@pytest.mark.asyncio
async def test_get_pizza_not_found_fails(pizza_repository, create_pizza):
    _ = create_pizza
    service = GetPizzaUseCase(pizza_repository)
    with pytest.raises(NotFoundError):
        await service.get_one("invalid_id")


@pytest.mark.asyncio
async def test_update_pizza_success(pizza_repository, create_pizza):
    _ = create_pizza
    service = UpdatePizzaUseCase(pizza_repository)
    data = UpdatePizzaInSchema(name="Margherita 2")

    await service.execute("123", data)

    pizza = await pizza_repository.find_one({"external_id": "123"})

    assert pizza["name"] == "Margherita 2"
    assert pizza["price"] == 30.0
    assert pizza["ingredients"] == ["tomato", "mozzarella"]


@pytest.mark.asyncio
async def test_delete_pizza_success(pizza_repository, create_pizza):
    _ = create_pizza
    service = DeletePizzaUseCase(pizza_repository)
    await service.execute("123")

    assert len(pizza_repository._data) == 0
