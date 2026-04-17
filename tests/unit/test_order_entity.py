import pytest
from src.domain.entities.order import Order
from src.core.exceptions import BadRequestError


def test_order_entity_creation_success():
    order = Order(name="Margherita", quantity=2, price=60.0)
    assert order.quantity == 2
    assert order.price == 60.0


def test_order_entity_invalid_quantity_fails():
    with pytest.raises(BadRequestError, match="Quantity must be greater than zero"):
        Order(name="Margherita", quantity=0, price=30.0)


def test_order_entity_invalid_price_fails():
    with pytest.raises(BadRequestError, match="Total price must be greater than zero"):
        Order(name="Margherita", quantity=1, price=0)
