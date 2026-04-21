import pytest

from src.domain.exceptions import BadRequestError, NotFoundError
from src.infrastructure.http.orders.schemas import CreateOrderInSchema
from src.use_cases.orders.create import CreateOrderUseCase
from src.use_cases.orders.get import GetOrderUseCase


@pytest.mark.asyncio
async def test_create_order_success(
    pizza_repository, store_repository, order_repository, create_pizza, create_store
):
    _ = (create_pizza, create_store)

    service = CreateOrderUseCase(order_repository, store_repository, pizza_repository)
    data = CreateOrderInSchema(name="Margherita", quantity=2)

    result = await service.execute(data)
    assert "order_external_id" in result


@pytest.mark.asyncio
async def test_create_order_insufficient_stock_fails(
    pizza_repository, store_repository, order_repository, create_pizza, create_store
):
    _ = (create_pizza, create_store)

    service = CreateOrderUseCase(order_repository, store_repository, pizza_repository)
    data = CreateOrderInSchema(name="Margherita", quantity=50)

    with pytest.raises(BadRequestError):
        await service.execute(data)


@pytest.mark.asyncio
async def test_get_order_success(
    order_repository, create_pizza, create_store, create_order
):
    _ = (create_pizza, create_store, create_order)

    service = GetOrderUseCase(order_repository)
    result = await service.get_one("123")

    assert result.get("quantity") == 2
    assert result.get("price") == 30.0


@pytest.mark.asyncio
async def test_get_order_not_found_fails(order_repository):

    service = GetOrderUseCase(order_repository)
    with pytest.raises(NotFoundError):
        await service.get_one("invalid_order_id")
