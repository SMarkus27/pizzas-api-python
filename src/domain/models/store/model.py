from pydantic import BaseModel


class StoreModel(BaseModel):
    name: str
    quantity: int
