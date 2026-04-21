from pydantic import BaseModel, Field


class CreatePizzaInSchema(BaseModel):
    name: str
    price: float
    ingredients: list[str]


class UpdatePizzaInSchema(BaseModel):
    name: str | None = Field(None)
    price: float | None = Field(None)
    ingredients: list[str] | None = Field(None)
