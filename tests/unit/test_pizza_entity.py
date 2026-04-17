import pytest
from src.domain.entities.pizza import Pizza
from src.core.exceptions import (
    InvalidNameError,
    InvalidPriceError,
    InvalidIngredientError,
)


def test_pizza_entity_creation_success():
    pizza = Pizza(name="Margherita", price=30.0, ingredients=["tomato", "mozzarella"])
    assert pizza.name == "Margherita"
    assert pizza.price == 30.0
    assert len(pizza.ingredients) == 2


def test_pizza_entity_invalid_name_fails():
    with pytest.raises(InvalidNameError):
        Pizza(name="Ab", price=30.0, ingredients=["tomato"])


def test_pizza_entity_invalid_price_fails():
    with pytest.raises(InvalidPriceError):
        Pizza(name="Margherita", price=0, ingredients=["tomato"])
    with pytest.raises(InvalidPriceError):
        Pizza(name="Margherita", price=-10.0, ingredients=["tomato"])


def test_pizza_entity_empty_ingredients_fails():
    with pytest.raises(InvalidIngredientError):
        Pizza(name="Margherita", price=30.0, ingredients=[])


def test_pizza_entity_short_ingredient_fails():
    with pytest.raises(InvalidIngredientError):
        Pizza(name="Margherita", price=30.0, ingredients=["to"])
