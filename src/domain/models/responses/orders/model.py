from src.domain.models.responses.base.model import BaseResponse


class OrdersResponse(BaseResponse):
    total_pages: int
