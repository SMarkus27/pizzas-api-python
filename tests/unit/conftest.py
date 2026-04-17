from datetime import datetime, timezone

import pytest

from tests.fakes.repository import FakeRepository


@pytest.fixture(scope="function")
async def pizza_repository():
    return FakeRepository()


@pytest.fixture(scope="function")
async def store_repository():
    return FakeRepository()


@pytest.fixture(scope="function")
async def order_repository():
    return FakeRepository()


@pytest.fixture(scope="function")
async def create_pizza(pizza_repository):
    doc = {
        "external_id": "123",
        "name": "Margherita",
        "price": 30.0,
        "ingredients": ["tomato", "mozzarella"],
        "created_at": datetime.now(timezone.utc),
        "updated_at": None,
    }
    await pizza_repository.insert_one(doc)
    return doc


@pytest.fixture(scope="function")
async def create_store(store_repository):
    doc = {
        "external_id": "123",
        "name": "Margherita",
        "quantity": 20,
        "created_at": datetime.now(timezone.utc),
        "updated_at": None,
    }
    await store_repository.insert_one(doc)
    return doc


@pytest.fixture(scope="function")
async def create_order(order_repository):
    doc = {
        "external_id": "123",
        "name": "Margherita",
        "price": 30.0,
        "quantity": 2,
        "created_at": datetime.now(timezone.utc),
        "updated_at": None,
    }
    await order_repository.insert_one(doc)
    return doc
