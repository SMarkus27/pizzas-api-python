import pytest
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# POST /api/orders/
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_order_success(
    async_client: AsyncClient,
    seed_pizza,
    seed_store,
    order_repo,
    store_repo,
):
    await seed_pizza(name="Margherita", price=30.0)
    await seed_store(name="Margherita", quantity=10)

    response = await async_client.post(
        "/api/orders/",
        json={
            "name": "Margherita",
            "quantity": 2,
        },
    )

    assert response.status_code == 201
    result = response.json()["data"]["result"]
    assert "order_external_id" in result

    order = await order_repo.find_one({"external_id": result["order_external_id"]})
    assert order is not None
    assert order["quantity"] == 2
    assert order["price"] == 60.0  # 30.0 * 2

    store = await store_repo.find_one({"name": "Margherita"})
    assert store["quantity"] == 8  # 10 - 2


@pytest.mark.asyncio
async def test_create_order_pizza_not_found_returns_404(
    async_client: AsyncClient,
    seed_store,
):
    # store existe mas pizza não está no cardápio
    await seed_store(name="Margherita", quantity=10)

    response = await async_client.post(
        "/api/orders/",
        json={
            "name": "Margherita",
            "quantity": 1,
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_order_no_store_item_returns_404(
    async_client: AsyncClient,
    seed_pizza,
):
    # pizza existe mas não há estoque
    await seed_pizza(name="Margherita")

    response = await async_client.post(
        "/api/orders/",
        json={
            "name": "Margherita",
            "quantity": 1,
        },
    )

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_order_empty_stock_returns_400(
    async_client: AsyncClient,
    seed_pizza,
    seed_store,
):
    await seed_pizza(name="Margherita")
    await seed_store(name="Margherita", quantity=0)

    response = await async_client.post(
        "/api/orders/",
        json={
            "name": "Margherita",
            "quantity": 1,
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_order_insufficient_stock_returns_400(
    async_client: AsyncClient,
    seed_pizza,
    seed_store,
):
    await seed_pizza(name="Margherita")
    await seed_store(name="Margherita", quantity=3)

    response = await async_client.post(
        "/api/orders/",
        json={
            "name": "Margherita",
            "quantity": 10,  # maior que o estoque
        },
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_order_invalid_quantity_returns_422(async_client: AsyncClient):
    response = await async_client.post(
        "/api/orders/",
        json={
            "name": "Margherita",
            "quantity": 0,  # deve ser maior que zero
        },
    )
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/orders/
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_all_orders_empty(async_client: AsyncClient):
    response = await async_client.get("/api/orders/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["items"] == []
    assert data["total_items"] == 0


@pytest.mark.asyncio
async def test_get_all_orders_with_data(async_client: AsyncClient, seed_order):
    await seed_order(name="Margherita", quantity=1, price=30.0)
    await seed_order(name="Pepperoni", quantity=2, price=70.0)

    response = await async_client.get("/api/orders/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_items"] == 2
    assert len(data["items"]) == 2


# ---------------------------------------------------------------------------
# GET /api/orders/{external_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_order_success(async_client: AsyncClient, seed_order):
    doc = await seed_order(name="Margherita", quantity=2, price=60.0)

    response = await async_client.get(f"/api/orders/{doc['external_id']}")

    assert response.status_code == 200
    result = response.json()["data"]["result"]
    assert result["external_id"] == doc["external_id"]
    assert result["name"] == "Margherita"
    assert result["price"] == 60.0
    assert result["quantity"] == 2


@pytest.mark.asyncio
async def test_get_order_not_found_returns_404(async_client: AsyncClient):
    response = await async_client.get("/api/orders/non-existent-id")
    assert response.status_code == 404
