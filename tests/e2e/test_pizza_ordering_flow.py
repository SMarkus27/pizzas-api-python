import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_complete_pizza_order_flow(async_client: AsyncClient):
    """
    End-to-end test for the whole pizza ordering flow:
    1. Create a store item for stock
    2. Create a pizza item
    3. Place an order for that pizza
    4. Verify stock decreased
    5. Get the order details
    """

    store_data = {"name": "Pepperoni", "quantity": 10}
    store_res = await async_client.post("/api/stores/", json=store_data)
    assert store_res.status_code == 201

    pizza_data = {
        "name": "Pepperoni",
        "price": 35.0,
        "ingredients": ["dough", "sauce", "cheese", "pepperoni"],
    }
    pizza_res = await async_client.post("/api/pizzas/", json=pizza_data)
    assert pizza_res.status_code == 201

    order_data = {"name": "Pepperoni", "quantity": 2}
    order_res = await async_client.post("/api/orders/", json=order_data)
    assert order_res.status_code == 201
    order_external_id = order_res.json()["data"]["result"]["order_external_id"]

    stores_list_res = await async_client.get("/api/stores/")
    store_items = stores_list_res.json()["data"]["items"]
    pepperoni_stock = next(item for item in store_items if item["name"] == "Pepperoni")
    assert pepperoni_stock["quantity"] == 8

    # 5. Get the order details to verify final price
    get_order_res = await async_client.get(f"/api/orders/{order_external_id}")
    assert get_order_res.status_code == 200
    order_details = get_order_res.json()["data"]["result"]
    # 35.0 * 2 = 70.0
    assert order_details["price"] == 70.0
    assert order_details["quantity"] == 2
    assert order_details["name"] == "Pepperoni"
