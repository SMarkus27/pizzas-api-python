import pytest

from src.domain.exceptions import BadRequestError, ConflictError, NotFoundError
from src.infrastructure.http.stores.schemas import CreateStoreInSchema, UpdateStoreInSchema
from src.use_cases.stores.create import CreateStoreUseCase
from src.use_cases.stores.update import UpdateStoreUseCase


@pytest.mark.asyncio
async def test_create_store_item_success(store_repository):
    service = CreateStoreUseCase(store_repository)
    data = CreateStoreInSchema(name="Margherita", quantity=100)

    result = await service.execute(data)

    assert "store_external_id" in result
    assert len(store_repository._data) == 1


@pytest.mark.asyncio
async def test_create_store_item_already_exists_fails(store_repository, create_store):
    _ = create_store
    service = CreateStoreUseCase(store_repository)
    data = CreateStoreInSchema(name="Margherita", quantity=100)

    with pytest.raises(ConflictError):
        await service.execute(data)


@pytest.mark.asyncio
async def test_increase_store_item_success(store_repository, create_store):
    _ = create_store
    service = UpdateStoreUseCase(store_repository)
    data = UpdateStoreInSchema(name="Margherita", quantity=5)

    await service.increase(data)

    store = await store_repository.find_one({"name": "Margherita"})

    assert store["name"] == "Margherita"
    assert store["quantity"] == 25


@pytest.mark.asyncio
async def test_decrease_store_item_success(store_repository, create_store):
    _ = create_store
    service = UpdateStoreUseCase(store_repository)
    data = UpdateStoreInSchema(name="Margherita", quantity=5)

    await service.decrease(data)

    store = await store_repository.find_one({"name": "Margherita"})

    assert store["name"] == "Margherita"
    assert store["quantity"] == 15


@pytest.mark.asyncio
async def test_decrease_store_item_insufficient_stock_fails(
    store_repository, create_store
):
    _ = create_store
    service = UpdateStoreUseCase(store_repository)
    data = UpdateStoreInSchema(name="Margherita", quantity=55)

    with pytest.raises(BadRequestError):
        await service.decrease(data)


@pytest.mark.asyncio
async def test_update_store_item_not_found_fails(store_repository, create_store):
    _ = create_store
    service = UpdateStoreUseCase(store_repository)
    data = UpdateStoreInSchema(name="Invalid", quantity=1)

    with pytest.raises(NotFoundError):
        await service.increase(data)


@pytest.mark.asyncio
async def test_decrease_store_item_empty_stock_fails(store_repository, create_store):
    _ = create_store
    service = UpdateStoreUseCase(store_repository)

    await store_repository.update_one({"name": "Margherita"}, {"quantity": 0})

    data = UpdateStoreInSchema(name="Margherita", quantity=1)

    with pytest.raises(BadRequestError):
        await service.decrease(data)
