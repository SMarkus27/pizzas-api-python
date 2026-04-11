from pydantic import BaseModel, Field, field_validator

from src.core.exceptions import InvalidIngredientError


MIN_INGREDIENT_LENGTH = 3


class UpdatePizzaInSchema(BaseModel):
    name: str | None = Field(None, min_length=3, max_length=100)
    price: float | None = Field(None, gt=0)
    ingredients: list[str] | None = Field(None, min_length=1)

    @field_validator("ingredients")
    @classmethod
    def validate_ingredients(cls, items: list[str]) -> list[str]:
        if items is None:
            return items
        for item in items:
            if len(item.strip()) < MIN_INGREDIENT_LENGTH:
                raise InvalidIngredientError()
        return [item.strip() for item in items]
