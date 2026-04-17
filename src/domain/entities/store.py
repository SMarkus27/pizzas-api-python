from dataclasses import dataclass

from src.core.exceptions import BadRequestError


@dataclass
class Store:
    name: str
    quantity: int

    def increase_quantity(self, amount: int) -> None:
        if amount <= 0:
            raise BadRequestError("Increase amount must be positive")
        self.quantity += amount

    def decrease_quantity(self, amount: int) -> None:
        if amount <= 0:
            raise BadRequestError("Decrease amount must be positive")

        if self.quantity == 0:
            raise BadRequestError("This product is empty")

        if amount > self.quantity:
            raise BadRequestError(
                f"Quantity to decrease ({amount}) must be less than or equal to current ({self.quantity})"
            )

        self.quantity -= amount
