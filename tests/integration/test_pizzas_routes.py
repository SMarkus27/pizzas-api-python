import pytest
from httpx import AsyncClient


# ---------------------------------------------------------------------------
# POST /api/pizzas/
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_create_pizza_success(async_client: AsyncClient, pizza_repo):
    pizza_data = {
        "name": "Margherita",
        "price": 30.0,
        "ingredients": ["tomato", "mozzarella", "basil"],
    }

    response = await async_client.post("/api/pizzas/", json=pizza_data)

    assert response.status_code == 201
    result = response.json()["data"]["result"]
    assert "pizza_external_id" in result

    pizza = await pizza_repo.find_one({"external_id": result["pizza_external_id"]})
    assert pizza is not None
    assert pizza["name"] == "Margherita"
    assert pizza["price"] == 30.0


@pytest.mark.asyncio
async def test_create_pizza_already_exists_returns_409(
    async_client: AsyncClient,
    seed_pizza,
):
    await seed_pizza(name="Margherita")

    response = await async_client.post(
        "/api/pizzas/",
        json={
            "name": "Margherita",
            "price": 40.0,
            "ingredients": ["extra cheese", "mozzarella"],
        },
    )

    assert response.status_code == 409
    assert "already exist" in response.json()["message"]


@pytest.mark.asyncio
async def test_create_pizza_invalid_name_returns_400(async_client: AsyncClient):
    response = await async_client.post(
        "/api/pizzas/",
        json={
            "name": "ab",
            "price": 30.0,
            "ingredients": ["tomato", "mozzarella"],
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_pizza_invalid_price_returns_400(async_client: AsyncClient):
    response = await async_client.post(
        "/api/pizzas/",
        json={
            "name": "Margherita",
            "price": -1.0,
            "ingredients": ["tomato", "mozzarella"],
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_pizza_short_ingredient_returns_400(async_client: AsyncClient):
    response = await async_client.post(
        "/api/pizzas/",
        json={
            "name": "Margherita",
            "price": 30.0,
            "ingredients": ["ab"],
        },
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_create_pizza_empty_ingredients_returns_400(async_client: AsyncClient):
    response = await async_client.post(
        "/api/pizzas/",
        json={
            "name": "Margherita",
            "price": 30.0,
            "ingredients": [],
        },
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# GET /api/pizzas/
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_all_pizzas_empty(async_client: AsyncClient):
    response = await async_client.get("/api/pizzas/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["result"] == []
    assert data["total_items"] == 0


@pytest.mark.asyncio
async def test_get_all_pizzas_with_data(async_client: AsyncClient, seed_pizza):
    await seed_pizza(name="Margherita", price=30.0)
    await seed_pizza(name="Pepperoni", price=35.0)

    response = await async_client.get("/api/pizzas/")

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["total_items"] == 2
    assert len(data["result"]) == 2


@pytest.mark.asyncio
async def test_get_all_pizzas_pagination(async_client: AsyncClient, seed_pizza):
    await seed_pizza(name="Pizza 1")
    await seed_pizza(name="Pizza 2")
    await seed_pizza(name="Pizza 3")

    response = await async_client.get("/api/pizzas/?page=1&size=2")

    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data["result"]) == 2
    assert data["total_items"] == 3
    assert data["total_pages"] == 2


@pytest.mark.asyncio
async def test_get_all_pizzas_invalid_page_returns_422(async_client: AsyncClient):
    response = await async_client.get("/api/pizzas/?page=0")  # page mínimo é 1
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# GET /api/pizzas/{external_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_get_pizza_success(async_client: AsyncClient, seed_pizza):
    doc = await seed_pizza(name="Margherita", price=30.0)

    response = await async_client.get(f"/api/pizzas/{doc['external_id']}")

    assert response.status_code == 200
    result = response.json()["data"]["result"]
    assert result["name"] == "Margherita"
    assert result["price"] == 30.0
    assert result["external_id"] == doc["external_id"]


@pytest.mark.asyncio
async def test_get_pizza_not_found_returns_404(async_client: AsyncClient):
    response = await async_client.get("/api/pizzas/non-existent-id")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# PUT /api/pizzas/{external_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_update_pizza_success(async_client: AsyncClient, seed_pizza, pizza_repo):
    doc = await seed_pizza(name="Margherita", price=30.0)

    response = await async_client.patch(
        f"/api/pizzas/{doc['external_id']}",
        json={
            "price": 45.0,
        },
    )

    assert response.status_code == 200

    updated = await pizza_repo.find_one({"external_id": doc["external_id"]})
    assert updated["price"] == 45.0
    assert updated["name"] == "Margherita"
    assert updated["updated_at"] is not None


@pytest.mark.asyncio
async def test_update_pizza_not_found_returns_404(async_client: AsyncClient):
    response = await async_client.patch(
        "/api/pizzas/non-existent-id",
        json={
            "price": 45.0,
        },
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_pizza_invalid_price_returns_400(
    async_client: AsyncClient,
    seed_pizza,
):
    doc = await seed_pizza()
    response = await async_client.patch(
        f"/api/pizzas/{doc['external_id']}",
        json={
            "price": -10.0,
        },
    )
    assert response.status_code == 400


# ---------------------------------------------------------------------------
# DELETE /api/pizzas/{external_id}
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_delete_pizza_success(async_client: AsyncClient, seed_pizza, pizza_repo):
    doc = await seed_pizza(name="Margherita")

    response = await async_client.delete(f"/api/pizzas/{doc['external_id']}")

    assert response.status_code == 200

    deleted = await pizza_repo.find_one({"external_id": doc["external_id"]})
    assert deleted is None


@pytest.mark.asyncio
async def test_delete_pizza_not_found_returns_404(async_client: AsyncClient):
    response = await async_client.delete("/api/pizzas/non-existent-id")
    assert response.status_code == 404
