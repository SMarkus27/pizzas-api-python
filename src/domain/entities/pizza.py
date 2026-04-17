from dataclasses import dataclass

from src.core.exceptions import (
    InvalidIngredientError,
    InvalidNameError,
    InvalidPriceError,
)


MIN_NAME_LENGTH = 3
MIN_INGREDIENT_LENGTH = 3


@dataclass
class Pizza:
    name: str
    price: float
    ingredients: list[str]

    def __post_init__(self):
        if len(self.name) < MIN_NAME_LENGTH:
            raise InvalidNameError()

        if self.price <= 0:
            raise InvalidPriceError(self.price)

        if not self.ingredients:
            raise InvalidIngredientError()

        for ingredient in self.ingredients:
            if len(ingredient) < MIN_INGREDIENT_LENGTH:
                raise InvalidIngredientError()
