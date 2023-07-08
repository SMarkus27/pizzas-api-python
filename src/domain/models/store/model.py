from pydantic import BaseModel


class StoreModel(BaseModel):
    pizza_name: str
    quantity: int
