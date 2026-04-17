import pytest
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# POST /api/stores/
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_store_item_success(async_client: AsyncClient, store_repo):
    response = await async_client.post(
        "/api/stores/",
        json={
            "name": "Mozzarella",
            "quantity": 50,
        },
    )

    assert response.status_code == 201
    result = response.json()["data"]["result"]
    assert "store_external_id" in result

    saved = await store_repo.find_one({"external_id": result["store_external_id"]})
    assert saved is not None
    assert saved["quantity"] == 50


@pytest.mark.asyncio
async def test_create_store_item_already_exists_returns_409(
    async_client: AsyncClient,
    seed_store,
):
    await seed_store(name="Mozzarella")

    response = await async_client.post(
        "/api/stores/",
        json={
            "name": "Mozzarella",
            "quantity": 10,
        },
    )

    assert response.status_code == 409


@pytest.mark.asyncio
async def test_create_store_item_invalid_quantity_returns_422(
    async_client: AsyncClient,
):
    response = await async_client.post(
        "/api/stores/",
        json={
            "name": "Mozzarella",
            "quantity": 0,
        },
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/stores/
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_all_store_items_empty(async_client: AsyncClient):
    response = await async_client.get("/api/stores/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == []
    assert data["total_items"] == 0


@pytest.mark.asyncio
async def test_get_all_store_items_with_data(async_client: AsyncClient, seed_store):
    await seed_store(name="Dough", quantity=100)
    await seed_store(name="Sauce", quantity=20)

    response = await async_client.get("/api/stores/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_items"] == 2
    assert len(data["items"]) == 2


# ---------------------------------------------------------------------------
# PATCH /api/stores/increase
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_increase_store_item_success(
    async_client: AsyncClient,
    seed_store,
    store_repo,
):
    doc = await seed_store(name="Cheese", quantity=100)

    response = await async_client.patch(
        "/api/stores/increase",
        json={
            "name": "Cheese",
            "quantity": 20,
        },
    )

    assert response.status_code == 200

    updated = await store_repo.find_one({"external_id": doc["external_id"]})
    assert updated["quantity"] == 120


# ---------------------------------------------------------------------------
# PATCH /api/stores/decrease
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_decrease_store_item_success(
    async_client: AsyncClient,
    seed_store,
    store_repo,
):
    doc = await seed_store(name="Cheese", quantity=100)

    response = await async_client.patch(
        "/api/stores/decrease",
        json={
            "name": "Cheese",
            "quantity": 20,
        },
    )

    assert response.status_code == 200

    updated = await store_repo.find_one({"external_id": doc["external_id"]})
    assert updated["quantity"] == 80


@pytest.mark.asyncio
async def test_decrease_store_item_not_found_returns_404(async_client: AsyncClient):
    response = await async_client.patch(
        "/api/stores/decrease",
        json={
            "name": "NonExistent",
            "quantity": 5,
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_decrease_store_item_insufficient_stock_returns_400(
    async_client: AsyncClient,
    seed_store,
):
    await seed_store(name="Cheese", quantity=10)

    response = await async_client.patch(
        "/api/stores/decrease",
        json={
            "name": "Cheese",
            "quantity": 50,
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_decrease_store_item_empty_stock_returns_400(
    async_client: AsyncClient,
    seed_store,
):
    await seed_store(name="Cheese", quantity=0)

    response = await async_client.patch(
        "/api/stores/decrease",
        json={
            "name": "Cheese",
            "quantity": 1,
        },
    )

    assert response.status_code == 400
