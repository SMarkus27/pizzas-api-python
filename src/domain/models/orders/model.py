from pydantic import BaseModel


class OrdersModel(BaseModel):
    name: str
    quantity: int
