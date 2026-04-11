from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator

from src.core.exceptions import InvalidIngredientException


class UpdatePizzaInSchema(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    ingredients: Optional[List[str]] = Field(None, min_length=1)

    @field_validator("ingredients")
    @classmethod
    def validate_ingredients(cls, items: list[str]) -> list[str]:
        for item in items:
            if len(item.strip()) < 3:
                raise InvalidIngredientException()
        return [item.strip() for item in items]