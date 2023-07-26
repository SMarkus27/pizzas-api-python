from typing import Union, List
from src.domain.models.responses.base.model import BaseResponse


class PizzasResponse(BaseResponse):
    total_pages: int
