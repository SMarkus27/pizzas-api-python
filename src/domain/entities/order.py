from dataclasses import dataclass

from src.core.exceptions import BadRequestError


@dataclass
class Order:
    name: str
    quantity: int
    price: float

    def __post_init__(self):
        if self.quantity <= 0:
            raise BadRequestError("Quantity must be greater than zero")
        if self.price <= 0:
            raise BadRequestError("Total price must be greater than zero")
