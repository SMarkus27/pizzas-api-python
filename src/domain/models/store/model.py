from pydantic import BaseModel, Field


class CreateStoreInSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    quantity: int = Field(..., gt=0)


class UpdateStoreInSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=100)
    quantity: int = Field(..., gt=0)
