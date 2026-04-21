from datetime import datetime, timezone
from uuid import uuid4

import pytest
from httpx import ASGITransport, AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from main import app
from src.infrastructure.mongodb.client import get_db
from src.infrastructure.mongodb.order_repository import OrderRepository
from src.infrastructure.mongodb.pizza_repository import PizzaRepository
from src.infrastructure.mongodb.store_repository import StoreRepository
from src.infrastructure.settings import get_settings


settings = get_settings()

@pytest.fixture
def mongo_client() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.MONGODB_CONNECTION_URL)
    yield client
    client.close()


@pytest.fixture
async def test_db(mongo_client: AsyncIOMotorClient) -> AsyncIOMotorClient:
    database = mongo_client[settings.MONGODB_DATABASE_TEST_NAME]

    await database["pizzas"].delete_many({})
    await database["stores"].delete_many({})
    await database["orders"].delete_many({})

    async def override_get_db():
        yield database

    app.dependency_overrides[get_db] = override_get_db

    yield database
    app.dependency_overrides.clear()


@pytest.fixture
async def async_client(test_db):
    _ = test_db
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture
def pizza_repo(test_db: AsyncIOMotorDatabase) -> PizzaRepository:
    return PizzaRepository(test_db)


@pytest.fixture
def store_repo(test_db: AsyncIOMotorDatabase) -> StoreRepository:
    return StoreRepository(test_db)


@pytest.fixture
def order_repo(test_db: AsyncIOMotorDatabase) -> OrderRepository:
    return OrderRepository(test_db)


@pytest.fixture
def seed_pizza(pizza_repo: PizzaRepository):
    async def _seed(
        name: str = "Margherita",
        price: float = 30.0,
        ingredients: list[str] | None = None,
    ) -> dict:
        doc = {
            "external_id": str(uuid4()),
            "name": name,
            "price": price,
            "ingredients": ingredients or ["tomato", "mozzarella"],
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
        }
        await pizza_repo.insert_one(doc)
        return doc

    return _seed


@pytest.fixture
def seed_store(store_repo: StoreRepository):
    async def _seed(
        name: str = "Margherita",
        quantity: int = 10,
    ) -> dict:
        doc = {
            "external_id": str(uuid4()),
            "name": name,
            "quantity": quantity,
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
        }
        await store_repo.insert_one(doc)
        return doc

    return _seed


@pytest.fixture
def seed_order(order_repo: OrderRepository):
    async def _seed(
        name: str = "Margherita",
        quantity: int = 1,
        price: float = 30.0,
    ) -> dict:
        doc = {
            "external_id": str(uuid4()),
            "name": name,
            "quantity": quantity,
            "price": price,
            "created_at": datetime.now(timezone.utc),
            "updated_at": None,
        }
        await order_repo.insert_one(doc)
        return doc

    return _seed
