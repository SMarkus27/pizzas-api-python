import pytest

from src.core.exceptions import BadRequestError, NotFoundError
from src.services.orders.create.schemas import CreateOrderInSchema
from src.services.orders.create.service import CreateOrderService
from src.services.orders.get_one.service import GetOrderService


@pytest.mark.asyncio
async def test_create_order_success(
    pizza_repository, store_repository, order_repository, create_pizza, create_store
):
    _ = (create_pizza, create_store)

    service = CreateOrderService(order_repository, store_repository, pizza_repository)
    data = CreateOrderInSchema(name="Margherita", quantity=2)

    result = await service.create(data)
    assert "order_external_id" in result


@pytest.mark.asyncio
async def test_create_order_insufficient_stock_fails(
    pizza_repository, store_repository, order_repository, create_pizza, create_store
):
    _ = (create_pizza, create_store)

    service = CreateOrderService(order_repository, store_repository, pizza_repository)
    data = CreateOrderInSchema(name="Margherita", quantity=50)

    with pytest.raises(BadRequestError):
        await service.create(data)


@pytest.mark.asyncio
async def test_get_order_success(
    order_repository, create_pizza, create_store, create_order
):
    _ = (create_pizza, create_store, create_order)

    service = GetOrderService(order_repository)
    result = await service.get_order("123")

    assert result.get("quantity") == 2
    # O preço total é pizza_price * quantity (30 * 2 = 60) no CreateOrderService,
    # mas a fixture create_order insere 30.0 diretamente.
    assert result.get("price") == 30.0


@pytest.mark.asyncio
async def test_get_order_not_found_fails(order_repository):

    service = GetOrderService(order_repository)
    with pytest.raises(NotFoundError):
        await service.get_order("invalid_order_id")
