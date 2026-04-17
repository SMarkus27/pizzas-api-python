from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    data: dict[str, Any] = {}
    status_code: int
    message: str | None = ""
