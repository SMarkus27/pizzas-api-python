from pydantic import BaseModel, Field


class UpdatePizzaInSchema(BaseModel):
    name: str | None = Field(None)
    price: float | None = Field(None)
    ingredients: list[str] | None = Field(None)
