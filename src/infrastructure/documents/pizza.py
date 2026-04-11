from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


@dataclass
class PizzaDocument:
    name: str
    price: float
    ingredients: list[str]
    external_id: str = field(default_factory=lambda: str(uuid4()))
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime | None = None

    def to_dict(self) -> dict:
        return {
            "external_id": self.external_id,
            "name": self.name,
            "price": self.price,
            "ingredients": self.ingredients,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
