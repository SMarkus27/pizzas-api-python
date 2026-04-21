import pytest
from src.domain.entities.store import Store
from src.domain.exceptions import BadRequestError


def test_store_entity_increase_success():
    store = Store(name="Cheese", quantity=10)
    store.increase_quantity(5)
    assert store.quantity == 15


def test_store_entity_increase_invalid_amount_fails():
    store = Store(name="Cheese", quantity=10)
    with pytest.raises(BadRequestError, match="Increase amount must be positive"):
        store.increase_quantity(0)


def test_store_entity_decrease_success():
    store = Store(name="Cheese", quantity=10)
    store.decrease_quantity(3)
    assert store.quantity == 7


def test_store_entity_decrease_more_than_available_fails():
    store = Store(name="Cheese", quantity=10)
    with pytest.raises(BadRequestError, match="must be less than or equal to current"):
        store.decrease_quantity(11)


def test_store_entity_decrease_empty_stock_fails():
    store = Store(name="Cheese", quantity=0)
    with pytest.raises(BadRequestError, match="This product is empty"):
        store.decrease_quantity(1)
