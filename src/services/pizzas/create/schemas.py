from pydantic import BaseModel


class CreatePizzaInSchema(BaseModel):
    name: str
    price: float
    ingredients: list[str]


class CreatePizzaOutSchema(BaseModel):
    external_id: str
