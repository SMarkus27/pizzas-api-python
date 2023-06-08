from typing import List

from pydantic import BaseModel


class PizzaModel(BaseModel):
    name: str
    price: float
    ingredients: List[str]
